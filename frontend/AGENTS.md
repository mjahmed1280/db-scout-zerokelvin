# Frontend: Scout Command Center (Streamlit)

## Role: Senior UI/UX Engineer (Streamlit Specialist)

## Task: Build the Data Dictionary Command Center

### 1. Visual Identity & Styling
- **Theme:** Professional dark theme with "Zero Kelvin" branding
- **Color Palette:** 
  - Primary: Cyan (#0ea5e9)
  - Secondary: Cyan Dark (#06b6d4)
  - Background: Slate Dark (#0f172a)
  - Surface: Slate (#1e293b)
  - Text: Slate Light (#f1f5f9)
- **Design Pattern:** Glassmorphism with semi-transparent containers
- **Typography:** Roboto Mono for status indicators and code blocks

### 2. Layout & Architecture

#### Sidebar: Scout Control Panel
- **Backend Connection Configuration**
  - Host input (default: 127.0.0.1)
  - Port number input (default: 8000)
  - LED-style status indicator showing API reachability
  
- **Database Connection Configuration**
  - Database type selector (PostgreSQL, SQL Server, Snowflake)
  - Host, Port, Database name, Username, Password inputs
  - Defaults: 127.0.0.1:5433, hackfest_db, hackfest/hackfest123
  - Status indicator (LED style) for database connectivity
  
- **Connect Button**
  - Primary action button
  - Triggers both API and database connectivity checks
  - Updates session state with connection status
  
- **System Status Metrics**
  - Backend API: Online/Offline with animation
  - Database: Online/Offline with animation
  - Real-time status updates

#### Main Content Area: Multi-Tab Interface

**Tab 1: 💬 Scout Chat**
- **Chat Interface**
  - `st.chat_message` components for user/assistant messages
  - Persistent chat history in `st.session_state`
  - Clear button to reset conversation
  
- **LangGraph Thinking Process**
  - `st.status` container showing agent steps:
    1. Parsing natural language query
    2. Extracting schema metadata
    3. Building knowledge graph
    4. Calculating statistical vitals
    5. Generating response
  - Progressive updates as each step completes
  - Estimated time displays
  
- **Streaming Response Support**
  - Real-time text display as backend streams response
  - Prevents "blank screen" user experience
  - Handles connection errors gracefully

**Tab 2: 🔗 ERD Visualizer**
- **Schema Selector**
  - Dropdown to choose: All, Olist, BikeStore, Public
  - Generate ERD button triggers backend
  
- **Mermaid.js Diagram Rendering**
  - Displays generated ERD code
  - Interactive visualization
  - Syntax-highlighted code view
  
- **Schema Metrics**
  - Total Tables count
  - Total Relationships count
  - Number of Schemas
  - Foreign Keys count
  - Data types distribution

**Tab 3: 📊 Data Health Dashboard**
- **Analyze Button**
  - Triggers full health analysis across all tables
  - Shows progress spinner
  
- **Health Metrics Cards**
  - Average Completeness %
  - Data Entropy (0-10 scale)
  - Outlier Detection count
  - Data Quality Score
  
- **High-Risk Columns Table**
  - Conditional formatting (color-coded Z-scores)
  - Columns with Z-Score > 3.0 highlighted
  - Outlier counts per column
  - Risk level indicators (🔴 High, 🟠 Medium, 🟡 Low)
  
- **Data Completeness Chart**
  - Bar chart showing completeness % per table
  - Color-coded by health status
  
- **Null Value Analysis**
  - Heatmap or table showing null distribution
  - Identifies problem columns
  
- **Summary Statistics**
  - Row counts per table
  - Schema size breakdown
  - Growth trends

**Tab 4: 📋 System Logs**
- **Live-Tailing Log View**
  - Reads from `backend/logs/system.jsonl`
  - Last 30 log entries displayed
  - Auto-refresh on trigger
  
- **Log Level Filter**
  - All, INFO, WARNING, ERROR filter
  - Conditional coloring per level
  
- **Log Display Format**
  - Timestamp (formatted)
  - Component (frontend, backend, ingestion-agent)
  - Operation name
  - Error messages (if applicable)
  - JSON pretty-print for details
  
- **Expanded Log Details**
  - Click to expand full JSON log entry
  - Shows all fields: steps, outputs, errors

### 3. Technical Implementation

#### Backend Client (`backend_client.py`)
- **HTTP Client Class**
  - Methods for health checks, queries, schema extraction
  - Error handling and timeout management
  - Async-ready architecture (future enhancement)
  
- **API Endpoints**
  - `/health` - Backend health check
  - `/database/test` - Database connectivity test
  - `/chat` - Natural language chat endpoint
  - `/schema/extract` - Full schema extraction
  - `/erd/generate` - ERD code generation
  - `/analysis/data-health` - Comprehensive health analysis
  - `/analysis/column-stats` - Detailed column statistics
  - `/lineage/table` - Table lineage and relationships
  - `/logs` - Retrieve system logs

#### Session State Management (`st.session_state`)
- `messages` - Chat message history
- `client` - Active BackendClient instance
- `connection_status` - Dict with api/db status booleans
- `chat_history` - Persistent conversation log
- `refresh_logs` - Flag to trigger log refresh

#### Configuration (`config.py`)
- Environment variable loading via `.env`
- Default values for all settings
- Feature flag management
- Theme and styling configuration

#### Utilities (`utils.py`)
- `Logger` class for frontend logging
- JSON formatting and parsing helpers
- Status indicator generation
- Risk color coding for statistics
- Timestamp formatting for display
- Connection string builders

### 4. Dependency Management

**Core Dependencies:**
- `streamlit>=1.28.0` - UI framework
- `requests>=2.31.0` - HTTP client
- `pandas>=2.0.0` - Data manipulation
- `plotly>=5.17.0` - Advanced charts
- `python-dateutil>=2.8.2` - Date handling
- `aiohttp>=3.9.0` - Async HTTP (future)

### 5. Development Workflow

#### Setup
```bash
cd frontend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

#### Run
```bash
streamlit run src/app.py
```

#### Access
- Local: http://127.0.0.1:8501
- Configure in sidebar
- Connect to backend

#### Testing
```bash
python -m pytest tests/ --cov=src
```

### 6. Logging Conventions

**All frontend actions logged to `/logs/frontend.jsonl`**

Example entries:
```json
{"timestamp": "2024-02-21T10:30:00Z", "component": "frontend", "level": "INFO", "operation": "connection_established", "details": {"api": true, "db": true}}
{"timestamp": "2024-02-21T10:31:15Z", "component": "frontend", "level": "INFO", "operation": "chat_query_sent", "details": {"query_length": 42, "schema_context": "olist"}}
{"timestamp": "2024-02-21T10:35:00Z", "component": "frontend", "level": "WARNING", "operation": "backend_timeout", "details": {"endpoint": "/chat", "timeout_seconds": 30}}
```

### 7. UI/UX Best Practices Applied

- **Immediate Feedback:** Spinners and status updates during operations
- **Progressive Disclosure:** Expand logs/details only when requested
- **Color Coding:** Health metrics use intuitive red/yellow/green
- **Responsive Design:** Sidebar collapses on mobile, tabs reorganize
- **Accessibility:** High contrast, semantic HTML, alt-text for charts
- **Error Recovery:** Graceful handling of connection failures with retry options
- **Performance:** Lazy loading of logs, pagination for large datasets

### 8. Future Enhancements

- [ ] WebSocket connection for real-time log streaming
- [ ] Advanced Plotly visualizations for embeddings/relationships
- [ ] Table-level drill-down for detailed column profiling
- [ ] Export chat history and analysis reports
- [ ] Role-based access control (RBAC)
- [ ] Dark/Light theme toggle
- [ ] Keyboard shortcuts for power users
- [ ] Query suggestion auto-complete
- [ ] Collaborative note-taking per table/column
- [ ] Custom alert thresholds for data quality metrics
  {
    "timestamp": "...",
    "component": "frontend.ui",
    "operation": "user_query",
    "inputs": { "query": "Show me the orders table" },
    "outputs": { "response_time_ms": 120 }
  }
  ```
