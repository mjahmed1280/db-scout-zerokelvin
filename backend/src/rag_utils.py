import os
import json
from datetime import datetime
from google.cloud import storage

# GCP & AI Imports
import vertexai
from vertexai import rag
from google import genai

# --- 1. SET UP CREDENTIALS ---
# Using an absolute path relative to this utils file
SA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "gcp-ragtester.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = SA_PATH

# GCP Configs
GCP_PROJECT_ID = os.getenv("GCP_PROJECT_ID", "gdc-ai-testing")
GCP_REGION = os.getenv("GCP_REGION", "asia-south1")
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "database-doc-bucket")

# Initialize Vertex AI
# Initialize both SDKs
vertexai.init(project=GCP_PROJECT_ID, location=GCP_REGION)

# New Unified Client initialization
ai_client = genai.Client(
    vertexai=True,
    project=GCP_PROJECT_ID,
    location=GCP_REGION
)

def upload_to_gcs(content: str, destination_blob_name: str, content_type: str = 'application/json') -> str:
    """Uploads a string (JSON or Markdown) to GCS."""
    client = storage.Client()
    bucket = client.bucket(GCS_BUCKET_NAME)
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_string(content, content_type=content_type)
    return f"gs://{GCS_BUCKET_NAME}/{destination_blob_name}"

def generate_markdown_doc(schema_name: str, json_report: dict) -> str:
    """Uses Gemini to generate Markdown documentation with an ERD."""
    prompt = f"""
    You are an expert Database Architect. I have generated a metadata and statistics JSON report for the '{schema_name}' schema.
    Please create a comprehensive Markdown (.md) documentation file.
    
    Include:
    1. A brief business context overview.
    2. A Mermaid.js ERD (Entity Relationship Diagram) showing how the tables connect.
    3. A clean breakdown of each table, its key columns, and any interesting statistical anomalies (like outliers or missing data).
    
    Here is the JSON data:
    {json.dumps(json_report)[:30000]}
    """
    response = ai_client.models.generate_content(
        model='gemini-2.5-flash',
        contents=prompt
    )
    return response.text

def create_rag_corpus(gcs_uri: str, user_id: str, schema_name: str) -> str:
    """Creates the Vertex AI RAG Corpus dynamically."""
    display_name = f"corpus_{user_id}_{schema_name}_{int(datetime.now().timestamp())}"
    
    embedding_config = rag.RagEmbeddingModelConfig(
        vertex_prediction_endpoint=rag.VertexPredictionEndpoint(publisher_model="publishers/google/models/text-embedding-005")
    )
    corpus = rag.create_corpus(
        display_name=display_name,
        backend_config=rag.RagVectorDbConfig(rag_embedding_model_config=embedding_config),
    )
    rag.import_files(
        corpus.name,
        [gcs_uri],
        transformation_config=rag.TransformationConfig(
            chunking_config=rag.ChunkingConfig(chunk_size=512, chunk_overlap=100)
        ),
    )
    return corpus.name

def search_rag_corpus(query: str, corpus_id: str) -> str:
    """A raw RAG search function that the ADK Agent uses as a Tool."""
    rag_retrieval_config = rag.RagRetrievalConfig(top_k=5)
    response = rag.retrieval_query(
        rag_resources=[rag.RagResource(rag_corpus=corpus_id)],
        text=query,
        rag_retrieval_config=rag_retrieval_config,
    )
    
    # Extract the relevant text chunks to return to the Agent
    if hasattr(response, "contexts") and response.contexts:
        chunks = [c.text for c in response.contexts.contexts]
        return "\n...\n".join(chunks)
    return "No relevant database documentation found."