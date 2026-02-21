# 🛰️ DB-Scout-ZeroKelvin

**The Agentic Reconnaissance Layer for Enterprise Data**

DB-Scout-ZeroKelvin transforms "data graveyards" into searchable knowledge bases. By leveraging the Model Context Protocol (MCP) and Agentic RAG, it autonomously scouts legacy databases, maps hidden relationships, and provides deep statistical intelligence—all while keeping your data private and secure.

![alt text](Doc/Gemini_Generated_Image_b3jjweb3jjweb3jj.png)
## 🚀 Core Pillars

**Standardized Recon (MCP Bridge):** Uses FastMCP to establish a secure, standardized bridge to SQL Server, PostgreSQL, and Snowflake.

**Topographical Mapping (In-Memory Graph):** Navigates complex table relationships using NetworkX to find optimal join paths and lineage.

**Deep Intel (Statistical Engine):** Beyond basic schema info, the Scout calculates Z-Scores for outlier detection and Shannon Entropy for data diversity.

**Zero-Trust Security:** Local-first transport layer ensures database credentials and PII never leave your private environment.

## 🏗️ Repository Structure

- **/mcp_server**: The "FastMCP" bridge connecting LLMs to the data terrain.
- **/scout_brain**: Core LangGraph logic, Agentic RAG orchestration, and NetworkX graph traversal.
- **/stats_engine**: Statistical analysis modules (Z-Scores, Entropy, Completeness).
- **/interface**: Streamlit-based "Scout Command Center" for natural language interrogation.
- **/reports**: Automated output of "Self-Healing" Markdown and JSON documentation.
- **/docs**: Architecture documentation and design specifications.
- **/logs**: Structured JSON logs for agent activities.
- **/scripts**: Helper scripts for setup and deployment.

## 🛠️ Quick Start

### 1. Initialize the Scout
```bash
# Create and activate environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install the Recon Stack
pip install -r requirements.txt
```

### 2. Configure the Mission
Create a `.env` file with your database credentials (stored locally and securely):
```
DB_TYPE=postgresql
DB_HOST=localhost
DB_PORT=5432
# DB-Scout uses these to build the local MCP bridge
```

### 3. Launch the Command Center
```bash
# Run the Scout Interface
streamlit run interface/app.py
```

## 📊 The "Scout" Analysis Workflow

**Ingestion:** Connects via MCP and extracts INFORMATION_SCHEMA.

**Profiling:** Samples 1,000 rows to calculate statistical "vitals."

**Mapping:** Generates Mermaid.js relationship diagrams.

**Reporting:** Produces AI-enhanced business summaries for every entity.

## 🛡️ Security & Privacy

**Read-Only Enforcement:** Code-level restrictions prevent any UPDATE/DELETE operations.

**Privacy-First RAG:** Raw data stays in the DB; only metadata and statistical samples are shared with the LLM to generate business context.

---

**Team Zero Kelvin** | GDG Cloud New Delhi × Turgon HackFest 2.0

See `AGENTS.md` for detailed agent guidelines and logging conventions.
