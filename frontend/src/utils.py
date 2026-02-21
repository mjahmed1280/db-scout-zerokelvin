"""
Utility functions for the Scout Command Center UI
"""

import streamlit as st
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List


class Logger:
    """Simple JSON logger for frontend operations."""
    
    def __init__(self, log_dir: str = "../../logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.log_file = self.log_dir / "frontend.jsonl"
    
    def log(self, level: str, operation: str, details: Dict[str, Any] = None):
        """Log an action to the frontend log file."""
        entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "component": "frontend",
            "level": level,
            "operation": operation,
            "details": details or {}
        }
        try:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            st.error(f"Failed to log: {str(e)}")
    
    def info(self, operation: str, details: Dict[str, Any] = None):
        """Log info level."""
        self.log("INFO", operation, details)
    
    def warning(self, operation: str, details: Dict[str, Any] = None):
        """Log warning level."""
        self.log("WARNING", operation, details)
    
    def error(self, operation: str, details: Dict[str, Any] = None):
        """Log error level."""
        self.log("ERROR", operation, details)


def format_json_string(json_str: str, indent: int = 2) -> str:
    """Format a JSON string for display."""
    try:
        parsed = json.loads(json_str)
        return json.dumps(parsed, indent=indent)
    except json.JSONDecodeError:
        return json_str


def get_status_indicator(status: bool) -> str:
    """Get a status indicator emoji."""
    return "🟢 Online" if status else "🔴 Offline"


def parse_log_line(log_line: str) -> Dict[str, Any]:
    """Parse a JSON log line."""
    try:
        return json.loads(log_line)
    except json.JSONDecodeError:
        return {
            "error": "Failed to parse log line",
            "raw": log_line
        }


def create_connection_string(db_config: Dict[str, Any]) -> str:
    """Create a connection string from database config."""
    db_type = db_config.get("type", "postgresql").lower()
    host = db_config.get("host", "localhost")
    port = db_config.get("port", 5432)
    database = db_config.get("database", "")
    user = db_config.get("user", "")
    
    if db_type == "postgresql":
        return f"postgresql://{user}@{host}:{port}/{database}"
    elif db_type == "sql server" or db_type == "mssql":
        return f"mssql+pyodbc://{user}@{host}:{port}/{database}"
    elif db_type == "snowflake":
        return f"snowflake://{user}@{host}/{database}"
    else:
        return f"{db_type}://{user}@{host}:{port}/{database}"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length."""
    if len(text) > max_length:
        return text[:max_length] + "..."
    return text


def format_timestamp(timestamp_str: str) -> str:
    """Format a timestamp string for display."""
    try:
        dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M:%S")
    except (ValueError, AttributeError):
        return timestamp_str


def get_risk_color(z_score: float) -> str:
    """Get color coding for risk levels based on Z-score."""
    if z_score > 3.5:
        return "🔴"  # Critical
    elif z_score > 3.0:
        return "🟠"  # High
    elif z_score > 2.5:
        return "🟡"  # Medium
    else:
        return "🟢"  # Low
