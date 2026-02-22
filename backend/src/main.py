import os
import sys
import json
import logging
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from fastapi import FastAPI, HTTPException, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy import create_engine, text
from dotenv import load_dotenv


load_dotenv(override=True)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- Import Internal Modules ---
from src.mcp_server import get_table_details, get_statistical_sample, list_tables, list_schemas, fetch_schemas_logic,engine
from src.rag_utils import upload_to_gcs, generate_markdown_doc, create_rag_corpus
from src.chat_agent import execute_chat  # Your modular ADK agent
from src.gcs_helper import download_file_from_gcs
from fastapi.responses import PlainTextResponse

# --- Logging Setup ---
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "component": "backend.api",
            "level": record.levelname,
            "operation": record.funcName,
            "message": record.getMessage()
        }
        if hasattr(record, "extra_data"):
            log_entry.update(record.extra_data)
        return json.dumps(log_entry)

logger = logging.getLogger("backend_api")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(os.path.join(LOG_DIR, "api_runs.jsonl"))
file_handler.setFormatter(JSONFormatter())
logger.addHandler(file_handler)

# --- FastAPI App ---
app = FastAPI(title="Intelligent Data Dictionary API", version="2.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

# --- Models ---
class AnalysisRequest(BaseModel):
    user_id: str
    schema_name: str
    db_config: Optional[Dict[str, Any]] = None

class ChatRequest(BaseModel):
    query: str
    rag_corpus_id: str
    session_id: str = "default_session"

class ChatResponse(BaseModel):
    response: str

class DBConfigRequest(BaseModel):
    config: Dict[str, Any]

# --- Endpoints ---
@app.get("/health")
def health_check():
    return {"status": "ok", "timestamp": datetime.now(timezone.utc).isoformat()}

@app.post("/database/test")
def test_database_connection(request: DBConfigRequest):
    try:
        cfg = request.config
        if cfg and "host" in cfg and "user" in cfg:
            db_url = f"postgresql://{cfg['user']}:{cfg.get('password', '')}@{cfg['host']}:{cfg.get('port', 5432)}/{cfg.get('database', '')}"
            temp_engine = create_engine(db_url)
            with temp_engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return {"status": "success", "message": "Successfully connected to the provided database!"}
        else:
            from src.mcp_server import engine
            with engine.connect() as conn:
                conn.execute(text("SELECT 1"))
            return {"status": "success", "message": "Connected to default server database."}
    except Exception as e:
        logger.error(f"Database connection failed: {str(e)}")
        raise HTTPException(status_code=400, detail=f"Connection failed: {str(e)}")

@app.get("/database/schemas")
async def get_schemas():
    try:
        # Call the logic function, not the @mcp.tool wrapped one
        schemas = fetch_schemas_logic()
        
        return {
            "status": "success",
            "count": len(schemas),
            "schemas": schemas
        }
    except Exception as e:
        logger.error(f"Failed to fetch schemas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")


@app.post("/analysis/run")
async def run_full_analysis(request: AnalysisRequest):
    """Generates federated DB Docs and creates the RAG Corpus."""
    user_id = request.user_id
    schema = request.schema_name
    timestamp = int(datetime.now().timestamp())
    
    try:
        # 1. Fetch tables
        tables = list_tables.fn(schema)
        if not tables:
            raise HTTPException(status_code=404, detail=f"No tables found in schema '{schema}'")

        from src.mcp_server import fetch_relationships_logic # Import the new logic
        relationships = fetch_relationships_logic(schema)
        full_report = {
            "schema": schema,
            "user_id": user_id,
            "analyzed_at": datetime.now(timezone.utc).isoformat(),
            "tables": {}
        }
        
        # 2. Extract Data via MCP
        for table in tables:
            logger.info(f"Analyzing table: {table}")
            full_report["tables"][table] = {
                "metadata": get_table_details.fn(table, schema),
                "statistics": get_statistical_sample.fn(table, schema)
            }
            
        # 3. Upload JSON to federated GCS path
        json_blob_name = f"{user_id}/{schema}/schema_analysis_{timestamp}.json"
        json_gcs_path = upload_to_gcs(json.dumps(full_report, indent=2), json_blob_name)
        
        # 4. Run MD Generation & RAG Corpus creation in parallel
        md_task = asyncio.to_thread(generate_markdown_doc, schema, full_report)
        rag_task = asyncio.to_thread(create_rag_corpus, json_gcs_path, user_id, schema)
        
        md_content, rag_corpus_id = await asyncio.gather(md_task, rag_task)
        
        # 5. Upload generated Markdown to the same subfolder
        md_blob_name = f"{user_id}/{schema}/schema_documentation_{timestamp}.md"
        md_gcs_path = upload_to_gcs(md_content, md_blob_name, content_type='text/markdown')
            
        return {
            "status": "success",
            "message": "Federated analysis, documentation, and RAG pipeline complete.",
            "json_gcs_path": json_gcs_path,
            "md_gcs_path": md_gcs_path,
            "rag_corpus_id": rag_corpus_id,
            "preview_tables": tables,
            "relationships": relationships
        }
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """Powers the chat UI using the ADK Agent with Memory."""
    try:
        # Delegate entirely to our modular ADK chat agent
        full_response = await execute_chat(
            query=request.query,
            rag_corpus_id=request.rag_corpus_id,
            session_id=request.session_id
        )
        return ChatResponse(response=full_response)

    except Exception as e:
        logger.error(f"ADK Chat error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"ADK Agent encountered an error: {str(e)}")

@app.get("/download")
async def download_secure_file(path: str = Query(..., description="The gs:// path from the AI Context")):
    """
    Secure proxy to fetch GCS files (Markdown/JSON) using the service account,
    and return the raw content to the frontend.
    """
    try:
        # 1. Fetch the file using our centralized helper function
        content = download_file_from_gcs(path)
        
        # 2. Return JSON cleanly if it's the schema JSON file
        if path.endswith('.json'):
            import json
            return json.loads(content)
            
        # 3. Return raw Markdown text for the Intelligence Docs
        return PlainTextResponse(content=content)
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except FileNotFoundError as fne:
        raise HTTPException(status_code=404, detail=str(fne))
    except Exception as e:
        logger.error(f"GCS Proxy Error for {path}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to retrieve secure file: {str(e)}")

@app.post("/erd/generate")
async def generate_erd(request: Request):
    """Generates an ASCII ERD dynamically."""
    body = await request.json()
    schema = body.get("schema", "public")
    try:
        print("feting tables...")
        tables = list_tables.fn(schema)
        erd = "erDiagram\n"
        for table in tables:
            erd += f"    {table.upper()} {{ }}\n"
        return {"erd_code": erd}
    except Exception as e:
         return {"erd_code": f"erDiagram\n %% Error: {str(e)}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)