"""
Configuration module for DB-Scout Frontend
"""

import os
from dotenv import load_dotenv

load_dotenv()

# Frontend Configuration
FRONTEND_HOST = os.getenv("FRONTEND_HOST", "127.0.0.1")
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", 8501))

# Backend Configuration
BACKEND_HOST = os.getenv("BACKEND_HOST", "127.0.0.1")
BACKEND_PORT = int(os.getenv("BACKEND_PORT", 8000))
BACKEND_URL = f"http://{BACKEND_HOST}:{BACKEND_PORT}"

# Database Configuration (Defaults)
DEFAULT_DB_TYPE = os.getenv("DB_TYPE", "postgresql")
DEFAULT_DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DEFAULT_DB_PORT = int(os.getenv("DB_PORT", 5433))
DEFAULT_DB_NAME = os.getenv("DB_NAME", "hackfest_db")
DEFAULT_DB_USER = os.getenv("DB_USER", "hackfest")
DEFAULT_DB_PASSWORD = os.getenv("DB_PASSWORD", "hackfest123")

# Logging Configuration
LOG_DIRECTORY = os.getenv("LOG_DIRECTORY", "../logs")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# UI Configuration
CHAT_HISTORY_LIMIT = int(os.getenv("CHAT_HISTORY_LIMIT", 50))
LOGS_DISPLAY_LIMIT = int(os.getenv("LOGS_DISPLAY_LIMIT", 30))
STREAM_TIMEOUT = int(os.getenv("STREAM_TIMEOUT", 60))

# Feature Flags
ENABLE_ADVANCED_VISUALIZATIONS = os.getenv("ENABLE_ADVANCED_VISUALIZATIONS", "true").lower() == "true"
ENABLE_REAL_TIME_LOGS = os.getenv("ENABLE_REAL_TIME_LOGS", "true").lower() == "true"
ENABLE_CHAT_STREAMING = os.getenv("ENABLE_CHAT_STREAMING", "true").lower() == "true"

# Styling
THEME = os.getenv("THEME", "dark")  # dark or light
PRIMARY_COLOR = os.getenv("PRIMARY_COLOR", "#0ea5e9")  # Cyan-500
SECONDARY_COLOR = os.getenv("SECONDARY_COLOR", "#06b6d4")  # Cyan-600
