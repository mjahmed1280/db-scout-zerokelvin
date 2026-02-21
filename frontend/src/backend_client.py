"""
Backend Client Utility for Scout Command Center
Handles async communication with the FastAPI backend and database connectivity checks.
"""

import requests
import json
from typing import Dict, Any, Optional
from urllib.parse import urljoin


class BackendClient:
    """Client for communicating with the DB-Scout backend API."""
    
    def __init__(self, host: str = "127.0.0.1", port: int = 8000, db_config: Optional[Dict[str, Any]] = None):
        """
        Initialize the backend client.
        
        Args:
            host: Backend API host
            port: Backend API port
            db_config: Database configuration dictionary
        """
        self.base_url = f"http://{host}:{port}"
        self.db_config = db_config or {}
        self.session = requests.Session()
        self.session.timeout = 10
    
    def check_backend(self) -> bool:
        """
        Check if backend API is reachable.
        
        Returns:
            True if backend is online, False otherwise
        """
        try:
            response = self.session.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except (requests.exceptions.RequestException, requests.exceptions.Timeout):
            return False
    
    def check_database(self) -> bool:
        """
        Check if database is reachable.
        
        Returns:
            True if database connection is successful, False otherwise
        """
        try:
            payload = {
                "action": "test_connection",
                "config": self.db_config
            }
            response = self.session.post(
                f"{self.base_url}/database/test",
                json=payload,
                timeout=10
            )
            return response.status_code == 200
        except (requests.exceptions.RequestException, requests.exceptions.Timeout):
            return False
    
    def send_query(self, query: str, stream: bool = False) -> Optional[Dict[str, Any]]:
        """
        Send a natural language query to the Scout agent.
        
        Args:
            query: Natural language query string
            stream: Whether to stream the response
        
        Returns:
            Response dictionary from the backend
        """
        try:
            payload = {
                "query": query,
                "db_config": self.db_config,
                "stream": stream
            }
            response = self.session.post(
                f"{self.base_url}/chat",
                json=payload,
                timeout=30,
                stream=stream
            )
            response.raise_for_status()
            
            if stream:
                # Handle streaming response
                for line in response.iter_lines():
                    if line:
                        yield json.loads(line)
            else:
                return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "success": False}
    
    def get_schema(self) -> Optional[Dict[str, Any]]:
        """
        Get the full database schema.
        
        Returns:
            Schema metadata dictionary
        """
        try:
            payload = {"db_config": self.db_config}
            response = self.session.post(
                f"{self.base_url}/schema/extract",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "success": False}
    
    def generate_erd(self, schema_name: Optional[str] = None) -> Optional[str]:
        """
        Generate an ERD (Entity Relationship Diagram) as Mermaid.js code.
        
        Args:
            schema_name: Optional schema to generate ERD for
        
        Returns:
            Mermaid.js diagram code string
        """
        try:
            payload = {
                "db_config": self.db_config,
                "schema": schema_name
            }
            response = self.session.post(
                f"{self.base_url}/erd/generate",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            result = response.json()
            return result.get("erd_code", "")
        except requests.exceptions.RequestException as e:
            return f"Error generating ERD: {str(e)}"
    
    def analyze_data_health(self) -> Optional[Dict[str, Any]]:
        """
        Analyze data health and statistics.
        
        Returns:
            Dictionary containing health metrics, Z-scores, entropy, etc.
        """
        try:
            payload = {"db_config": self.db_config}
            response = self.session.post(
                f"{self.base_url}/analysis/data-health",
                json=payload,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "success": False}
    
    def get_column_statistics(self, table: str, column: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed statistics for a specific column.
        
        Args:
            table: Table name
            column: Column name
        
        Returns:
            Statistics dictionary (Z-scores, outliers, entropy, etc.)
        """
        try:
            payload = {
                "db_config": self.db_config,
                "table": table,
                "column": column
            }
            response = self.session.post(
                f"{self.base_url}/analysis/column-stats",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "success": False}
    
    def get_table_lineage(self, table: str) -> Optional[Dict[str, Any]]:
        """
        Get table lineage and relationships.
        
        Args:
            table: Table name
        
        Returns:
            Lineage information including parent/child tables
        """
        try:
            payload = {
                "db_config": self.db_config,
                "table": table
            }
            response = self.session.post(
                f"{self.base_url}/lineage/table",
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e), "success": False}
    
    def get_logs(self, limit: int = 50) -> Optional[list]:
        """
        Get recent system logs from the backend.
        
        Args:
            limit: Maximum number of log entries to retrieve
        
        Returns:
            List of log entries
        """
        try:
            params = {"limit": limit}
            response = self.session.get(
                f"{self.base_url}/logs",
                params=params,
                timeout=10
            )
            response.raise_for_status()
            return response.json().get("logs", [])
        except requests.exceptions.RequestException as e:
            return [{"error": str(e)}]
