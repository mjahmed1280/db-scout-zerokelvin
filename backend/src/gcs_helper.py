import os
import json
from google.oauth2 import service_account
from google.cloud import storage

# Path to your service account JSON file
SA_KEY_PATH = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "gcp-gcs-fb.json")
GCS_BUCKET_NAME = os.getenv("GCS_BUCKET_NAME", "database-doc-bucket")

def upload_dict_to_gcs(data: dict, destination_blob_name: str) -> str:
    """Uploads a dictionary as a JSON file to a GCS bucket."""
    try:
        credentials = service_account.Credentials.from_service_account_file(SA_KEY_PATH)
        client = storage.Client(credentials=credentials)
        bucket = client.bucket(GCS_BUCKET_NAME)
        blob = bucket.blob(destination_blob_name)

        # Upload JSON string
        blob.upload_from_string(
            data=json.dumps(data, indent=2, default=str),
            content_type='application/json'
        )
        
        # Return the public/accessible URL (or gs:// path if private)
        return f"gs://{GCS_BUCKET_NAME}/{destination_blob_name}"
    except Exception as e:
        print(f"Error uploading to GCS: {e}")
        return None

def download_file_from_gcs(gcs_path: str) -> str:
    """Downloads a file from a GCS gs:// path and returns its content as a string."""
    if not gcs_path.startswith("gs://"):
        raise ValueError("Invalid path. Must start with gs://")

    # Parse bucket and blob name
    # Example: gs://database-doc-bucket/local_dev/bikestore/schema_doc.md -> bucket, blob
    path_without_prefix = gcs_path[5:]
    try:
        bucket_name, blob_name = path_without_prefix.split("/", 1)
    except ValueError:
        raise ValueError("Malformed GCS path. Expected gs://<bucket_name>/<blob_path>")
        
    # Authenticate EXACTLY like the upload function does
    credentials = service_account.Credentials.from_service_account_file(SA_KEY_PATH)
    client = storage.Client(credentials=credentials)
    
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    if not blob.exists():
        raise FileNotFoundError(f"File not found in GCS: {gcs_path}")
        
    # Download and return as raw text
    return blob.download_as_text()
    
# Awesome! Integrating this RAG corpus creation directly into your backend pipeline 
# is exactly how you make this system production-ready. 
# This ensures that every time a user requests an analysis for a specific schema, 
# the backend automatically generates the JSON, uploads it to GCS, 
# builds the vector database, and returns the unique ID for that specific dataset.