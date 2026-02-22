# Intelligent Data Dictionary Agent - Global Agent Instructions

## 1. Project Context
This project is an "Intelligent Data Dictionary Agent" for HackFest 2.0. It connects to PostgreSQL databases, extracts schema metadata using FastMCP, processes it via LangGraph, and visualizes it in a Streamlit frontend.

**Core Components:**
- **Frontend:** Streamlit-based UI (`/frontend`).
- **Backend:** Python-based FastMCP server & LangGraph orchestration (`/backend`).
- **Database:** PostgreSQL (existing container `hackfest-postgres-final`).

## 2. Global Conventions
- **Code Style:** Python (PEP 8), TypeScript/JavaScript (Standard).
- **Paths:** Always use relative paths from the project root or component root.
- **Environment:** Use `.env` files for configuration.
- **Documentation:** Maintain `README.md` and `AGENTS.md` in each component.

## 3. Setup & Build
- **Prerequisites:** Docker, Python 3.10+, Node.js (if applicable).
- **Global Build:** `docker-compose up --build`

## 4. Logging Conventions
All agent actions must be logged in structured JSON format to `/logs/`.

**File Naming:**
- `agent_runs.jsonl`: General agent activity.
- `ingestion.jsonl`: Schema extraction logs.
- `processing.jsonl`: Analysis and processing logs.
- `error.jsonl`: Error logs.

**Log Format (JSON Lines):**
Each line must be a valid JSON object with the following fields:
- `timestamp`: ISO8601 string (e.g., "2023-10-27T10:00:00Z").
- `component`: "frontend", "backend", "ingestion-agent", etc.
- `level`: "INFO", "WARNING", "ERROR".
- `operation`: The specific action being performed (e.g., "extract_schema", "generate_erd").
- `steps`: List of steps taken (optional but recommended for complex ops).
- `outputs`: Result of the operation.
- `error`: Error message (if applicable).

**Example:**
```json
{"timestamp": "2023-10-27T10:00:00Z", "component": "backend", "level": "INFO", "operation": "list_schemas", "outputs": ["public", "sales", "production"]}
{"timestamp": "2023-10-27T10:05:00Z", "component": "ingestion-agent", "level": "ERROR", "operation": "connect_db", "error": "Connection refused"}
```

## 5. Development Workflow
1.  **Read:** Always read `AGENTS.md` in the directory you are working in.
2.  **Plan:** outline your changes.
3.  **Implement:** Write code.
4.  **Verify:** Run tests (see component `AGENTS.md`).
5.  **Log:** Log your major actions to `logs/agent_runs.jsonl`.
