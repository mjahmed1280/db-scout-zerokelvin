"""
Fast API Test Endpoints for MCP Server Connectivity
This file exposes the mcp_server functions as REST API endpoints for testing.
"""

import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
import uvicorn
from sqlalchemy import text

# Add parent directory to path for imports
current_dir = Path(__file__).resolve().parent
src_path = current_dir.parent / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

try:
    from mcp_server import (
        list_schemas,
        list_tables,
        get_table_details,
        get_statistical_sample,
        run_sql_query,
        log_action,
        engine,
        DATABASE_URL
    )
except ImportError as e:
    print(f"Error: Could not import mcp_server. Ensure your path is correct: {e}")
    sys.exit(1)

app = FastAPI(
    title="MCP Server Test API",
    description="Test endpoints for Database Schema Extraction",
    version="1.0.0"
)

security = HTTPBasic()

API_USERNAME = os.getenv("API_USER", "hackfest")
API_PASSWORD = os.getenv("API_PASS", "hackfest123")

def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.username != API_USERNAME or credentials.password != API_PASSWORD:
        log_action("auth_failed", {"username": credentials.username}, "Invalid credentials")
        raise HTTPException(
            status_code=401,
            detail="Invalid API credentials",
            headers={"WWW-Authenticate": "Basic"}
        )
    return credentials.username

# --- Pydantic models ---
class SchemaResponse(BaseModel):
    schemas: List[str]
    status: str

class TablesResponse(BaseModel):
    schema_name: str
    tables: List[str]
    status: str

class TableDetailsResponse(BaseModel):
    table_name: str
    schema_name: str
    details: Dict[str, Any]
    status: str

class StatisticalSampleResponse(BaseModel):
    table_name: str
    schema_name: str
    statistics: Dict[str, Any]
    status: str

class SQLQueryRequest(BaseModel):
    query: str

class SQLQueryResponse(BaseModel):
    query: str
    rows: List[Dict[str, Any]]
    status: str

class ConnectionTestResponse(BaseModel):
    status: str
    message: str
    database_host: str
    database_name: str

# --- Endpoints ---

@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "MCP Server Test API is running",
        "version": "1.0.0",
        "endpoints": ["/test-connection", "/schemas", "/tables/{schema}", "/table-details/{schema}/{table}", "/statistical-sample/{schema}/{table}", "/sql-query"]
    }

@app.get("/test-connection", response_model=ConnectionTestResponse, tags=["Connection"])
async def test_connection(username: str = Depends(verify_credentials)):
    try:
        db_pass = os.getenv("DB_PASSWORD", "hackfest")
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            return {
                "status": "success",
                "message": "Connected to database successfully",
                "database_host": os.getenv("DB_HOST", "localhost"),
                "database_name": os.getenv("DB_NAME", "hackfest_db")
            }
    except Exception as e:
        error_msg = str(e)
        raise HTTPException(status_code=500, detail={"status": "failed", "error": error_msg})

@app.get("/schemas", response_model=SchemaResponse, tags=["Schema"])
async def get_schemas(username: str = Depends(verify_credentials)):
    try:
        schemas = list_schemas.fn() 
        return {"schemas": schemas, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tables/{schema_name}", response_model=TablesResponse, tags=["Tables"])
async def get_tables(schema_name: str, username: str = Depends(verify_credentials)):
    try:
        tables = list_tables.fn(schema_name)
        return {"schema_name": schema_name, "tables": tables, "status": "success"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/table-details/{schema_name}/{table_name}", response_model=TableDetailsResponse, tags=["Table Details"])
async def get_details(schema_name: str, table_name: str, username: str = Depends(verify_credentials)):
    try:
        # Use .fn for the Tool object
        details = get_table_details.fn(table_name, schema_name)
        return {
            "schema_name": schema_name,
            "table_name": table_name,
            "details": details,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/statistical-sample/{schema_name}/{table_name}", response_model=StatisticalSampleResponse, tags=["Statistics"])
async def get_stats(schema_name: str, table_name: str, username: str = Depends(verify_credentials)):
    try:
        # Use .fn for the Tool object
        stats = get_statistical_sample.fn(table_name, schema_name)
        return {
            "schema_name": schema_name,
            "table_name": table_name,
            "statistics": stats,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/sql-query", response_model=SQLQueryResponse, tags=["Query"])
async def execute_sql(request: SQLQueryRequest, username: str = Depends(verify_credentials)):
    if not request.query.lower().strip().startswith("select"):
        raise HTTPException(status_code=400, detail="Only SELECT queries are allowed")
    try:
        # Use .fn for the Tool object
        rows = run_sql_query.fn(request.query)
        return {
            "query": request.query,
            "rows": rows,
            "status": "success"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def run_server(host: str = "0.0.0.0", port: int = 8000):
    uvicorn.run(app, host=host, port=port)

if __name__ == "__main__":
    run_server()