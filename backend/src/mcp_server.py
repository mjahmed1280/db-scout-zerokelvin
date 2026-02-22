import os
import logging
import json
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from sqlalchemy import create_engine, text
from fastmcp import FastMCP
from dotenv import load_dotenv
from scipy.stats import zscore
import numpy as np

# Load environment variables
load_dotenv(override=True)

# Configure structured logging
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "logs")
os.makedirs(LOG_DIR, exist_ok=True)

class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "component": "backend.mcp_server",
            "level": record.levelname,
            "operation": record.funcName,
            "message": record.getMessage()
        }
        if hasattr(record, "extra_data"):
            log_entry.update(record.extra_data)
        return json.dumps(log_entry)

logger = logging.getLogger("mcp_server")
logger.setLevel(logging.INFO)
file_handler = logging.FileHandler(os.path.join(LOG_DIR, "ingestion.jsonl"))
file_handler.setFormatter(JSONFormatter())
logger.addHandler(file_handler)

# Database Configuration
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5433")
DB_USER = os.getenv("DB_USER", "hackfest")
DB_PASSWORD = os.getenv("DB_PASSWORD", "hackfest")
DB_NAME = os.getenv("DB_NAME", "hackfest_db")
DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Initialize FastMCP Server
mcp = FastMCP("IntelligentDataDictionary")

# Initialize Database Engine
engine = create_engine(DATABASE_URL)

def log_action(operation: str, outputs: Any, error: Optional[str] = None):
    extra = {"operation": operation, "outputs": outputs, "error": error}
    logger.info("Action executed", extra={"extra_data": extra})


# @mcp.tool()
# def list_schemas() -> List[str]:
#     """Lists all available schemas in the database."""
#     try:
#         with engine.connect() as conn:
#             query = text("SELECT schema_name FROM information_schema.schemata WHERE schema_name NOT IN ('information_schema', 'pg_catalog')")
#             result = conn.execute(query).fetchall()
#             schemas = [row[0] for row in result]
#             log_action("list_schemas", schemas)
#             return schemas
#     except Exception as e:
#         log_action("list_schemas", None, str(e))
#         return []

@mcp.tool()
def list_tables(schema_name: str) -> List[str]:
    """Lists tables for a specific schema."""
    try:
        with engine.connect() as conn:
            query = text("SELECT table_name FROM information_schema.tables WHERE table_schema = :schema")
            result = conn.execute(query, {"schema": schema_name}).fetchall()
            tables = [row[0] for row in result]
            log_action("list_tables", tables)
            return tables
    except Exception as e:
        log_action("list_tables", None, str(e))
        return []

@mcp.tool()
def get_table_details(table_name: str, schema_name: str) -> Dict[str, Any]:
    """Gets columns, types, and primary/foreign key metadata for a table."""
    try:
        with engine.connect() as conn:
            # Columns
            col_query = text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_schema = :schema AND table_name = :table
            """)
            columns = [dict(row._mapping) for row in conn.execute(col_query, {"schema": schema_name, "table": table_name})]
            
            # Primary Keys
            pk_query = text("""
                SELECT kcu.column_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu
                  ON tc.constraint_name = kcu.constraint_name
                  AND tc.table_schema = kcu.table_schema
                WHERE tc.constraint_type = 'PRIMARY KEY'
                  AND tc.table_schema = :schema
                  AND tc.table_name = :table
            """)
            pks = [row[0] for row in conn.execute(pk_query, {"schema": schema_name, "table": table_name})]

            # Foreign Keys
            fk_query = text("""
                SELECT
                    kcu.column_name,
                    ccu.table_schema AS foreign_table_schema,
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name
                FROM information_schema.table_constraints AS tc
                JOIN information_schema.key_column_usage AS kcu
                  ON tc.constraint_name = kcu.constraint_name
                  AND tc.table_schema = kcu.table_schema
                JOIN information_schema.constraint_column_usage AS ccu
                  ON ccu.constraint_name = tc.constraint_name
                  AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY'
                  AND tc.table_schema = :schema
                  AND tc.table_name = :table
            """)
            fks = [dict(row._mapping) for row in conn.execute(fk_query, {"schema": schema_name, "table": table_name})]

            details = {"columns": columns, "primary_keys": pks, "foreign_keys": fks}
            log_action("get_table_details", details)
            return details
    except Exception as e:
        log_action("get_table_details", None, str(e))
        return {}

def calculate_shannon_entropy(series):
    """Calculates Shannon Entropy for column uniqueness."""
    import math
    counts = series.value_counts()
    entropy = -sum((count / len(series)) * math.log(count / len(series), 2) for count in counts)
    return entropy

# @mcp.tool()
# def get_statistical_sample(table_name: str, schema_name: str) -> Dict[str, Any]:
#     """Performs a smart 1,000-row sample to calculate entropy, z-scores, and missing values."""
#     try:
#         query = f'SELECT * FROM "{schema_name}"."{table_name}" LIMIT 1000'
#         df = pd.read_sql(query, engine)
        
#         stats = {}
#         for col in df.columns:
#             col_stats = {
#                 "missing_percentage": df[col].isnull().mean() * 100,
#                 "entropy": calculate_shannon_entropy(df[col]) if df[col].dtype == 'object' or df[col].dtype == 'string' else None
#             }
            
#             if pd.api.types.is_numeric_dtype(df[col]):
#                 # Calculate Z-Scores
#                 df_clean = df[col].dropna()
#                 if not df_clean.empty and df_clean.std() > 0:
#                     z_scores = np.abs(zscore(df_clean))
#                     outliers = int((z_scores > 3).sum())
#                     col_stats["outliers_count"] = outliers
#                     col_stats["z_score_max"] = float(z_scores.max())
#                 else:
#                      col_stats["outliers_count"] = 0
#                      col_stats["z_score_max"] = 0.0

#             stats[col] = col_stats
            
#         log_action("get_statistical_sample", stats)
#         return stats
#     except Exception as e:
#         log_action("get_statistical_sample", None, str(e))
#         return {"error": str(e)}

@mcp.tool()
def get_statistical_sample(table_name: str, schema_name: str) -> Dict[str, Any]:
    """Performs a smart 1,000-row sample and returns table-wide stats for Data Vitals."""
    try:
        # 1. Get total row count (Crucial for Data Vitals charts)
        count_query = f'SELECT COUNT(*) FROM "{schema_name}"."{table_name}"'
        with engine.connect() as conn:
            total_rows = conn.execute(text(count_query)).scalar()

        # 2. Get sample for column analysis
        query = f'SELECT * FROM "{schema_name}"."{table_name}" LIMIT 1000'
        df = pd.read_sql(query, engine)
        
        column_results = {}
        for col in df.columns:
            col_stats = {
                "missing_percentage": df[col].isnull().mean() * 100,
                "entropy": calculate_shannon_entropy(df[col]) if df[col].dtype in ['object', 'string'] else None,
                "outliers_detected": 0 # Default key expected by frontend
            }
            
            if pd.api.types.is_numeric_dtype(df[col]):
                df_clean = df[col].dropna()
                if not df_clean.empty and df_clean.std() > 0:
                    z_scores = np.abs(zscore(df_clean))
                    col_stats["outliers_detected"] = int((z_scores > 3).sum())
                    col_stats["z_score_max"] = float(z_scores.max())

            column_results[col] = col_stats
            
        # 3. Return structured object expected by run_full_analysis
        result = {
            "row_count": total_rows,
            "column_stats": column_results
        }
        
        log_action("get_statistical_sample", result)
        return result
    except Exception as e:
        log_action("get_statistical_sample", None, str(e))
        return {"error": str(e), "row_count": 0, "column_stats": {}}


@mcp.tool()
def run_sql_query(query: str) -> List[Dict[str, Any]]:
    """Runs a read-only SQL query."""
    if not query.lower().startswith("select"):
        log_action("run_sql_query", None, "Only SELECT queries are allowed.")
        return [{"error": "Only SELECT queries are allowed."}]
    
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            rows = [dict(row._mapping) for row in result]
            log_action("run_sql_query", f"Returned {len(rows)} rows")
            return rows
    except Exception as e:
        log_action("run_sql_query", None, str(e))
        return [{"error": str(e)}]

# 1. Define the logic in a standard Python function
def fetch_schemas_logic() -> List[str]:
    """Internal logic to list schemas."""
    try:
        with engine.connect() as conn:
            query = text("""
                SELECT schema_name FROM information_schema.schemata 
                WHERE schema_name NOT IN ('information_schema', 'pg_catalog')
            """)
            result = conn.execute(query).fetchall()
            schemas = [row[0] for row in result]
            log_action("list_schemas", schemas)
            return schemas
    except Exception as e:
        log_action("list_schemas", None, str(e))
        return []

# 2. Point the MCP tool to that logic
@mcp.tool()
def list_schemas() -> List[str]:
    """Lists all available schemas in the database."""
    return fetch_schemas_logic()

# Add this function to src/mcp_server.py
def fetch_relationships_logic(schema: str):
    """Retrieves Foreign Key metadata from PostgreSQL information_schema."""
    query = text("""
        SELECT
            kcu.table_name AS source_table,
            rel_kcu.table_name AS target_table,
            kcu.column_name AS source_column
        FROM information_schema.table_constraints tco
        JOIN information_schema.key_column_usage kcu
          ON tco.constraint_name = kcu.constraint_name
        JOIN information_schema.referential_constraints rco
          ON tco.constraint_name = rco.constraint_name
        JOIN information_schema.key_column_usage rel_kcu
          ON rco.unique_constraint_name = rel_kcu.constraint_name
        WHERE tco.constraint_type = 'FOREIGN KEY' 
          AND tco.table_schema = :schema
    """)
    try:
        with engine.connect() as conn:
            result = conn.execute(query, {"schema": schema})
            return [dict(row._mapping) for row in result]
    except Exception as e:
        log_action("fetch_relationships", None, str(e))
        return []

if __name__ == "__main__":
    mcp.run()
