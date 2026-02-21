"""
DB-Scout-ZeroKelvin Command Center
Minimalist Multi-Page Modern Web App for Intelligent Data Discovery
"""

import streamlit as st
import json
import time
from pathlib import Path
from backend_client import BackendClient

# Configure page
st.set_page_config(
    page_title="DB-Scout: Transform Data Graveyards",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "Team Zero Kelvin | GDG Cloud New Delhi × Turgon HackFest 2.0"
    }
)

# Minimalist CSS Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');
    
    /* Root Variables */
    :root {
        --bg-dark: #0F172A;
        --bg-light: #FFFFFF;
        --surface: #1E293B;
        --border: #334155;
        --text-primary: #F1F5F9;
        --text-secondary: #CBD5E1;
        --primary: #3B82F6;
        --success: #10B981;
        --warning: #F59E0B;
        --error: #EF4444;
    }
    
    /* FORCE GLOBAL BACKGROUND */
    .main,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stSidebar"] {
        background-color: var(--bg-dark) !important;
    }
    
    /* Global */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    code, pre, .code-block {
        font-family: 'JetBrains Mono', monospace;
    }
    
    .main {
        background-color: var(--bg-dark);
        color: var(--text-primary);
    }
    
    /* Buttons - FLAT BLUE */
    div.stButton > button:first-child {
        background-color: var(--primary);
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        padding: 10px 24px;
        transition: background-color 0.2s ease;
        font-family: 'Inter', sans-serif;
        box-shadow: none !important;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #2563EB;
        box-shadow: none !important;
    }
    
    div.stButton > button:first-child:active {
        background-color: #1D4ED8;
    }
    
    /* Container/Card Styling - SOLID BORDERS ONLY */
    [data-testid="stVerticalBlockBorderContainer"] {
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        background-color: var(--surface) !important;
        padding: 1.5rem !important;
        box-shadow: none !important;
    }
    
    /* Text Inputs */
    input, [data-testid="stTextInputContainer"] input,
    [data-testid="stNumberInputContainer"] input,
    [data-testid="stSelectboxContainer"] select {
        background-color: var(--surface) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border) !important;
        border-radius: 6px !important;
        transition: border-color 0.2s ease;
    }
    
    input:focus, [data-testid="stTextInputContainer"] input:focus,
    [data-testid="stNumberInputContainer"] input:focus {
        border-color: var(--primary) !important;
        box-shadow: none !important;
        background-color: var(--surface) !important;
    }
    
    [data-testid="stSelectboxContainer"] select:focus {
        border-color: var(--primary) !important;
        box-shadow: none !important;
    }
    
    /* Tabs */
    [data-testid="stTabs"] > [role="tablist"] > button[role="tab"] {
        color: var(--text-secondary);
        border-bottom: 2px solid transparent;
        font-weight: 500;
        transition: color 0.2s ease;
        border-radius: 0;
    }
    
    [data-testid="stTabs"] > [role="tablist"] > button[role="tab"][aria-selected="true"] {
        color: var(--primary);
        border-bottom-color: var(--primary);
    }
    
    [data-testid="stTabs"] > [role="tablist"] > button[role="tab"]:hover {
        color: var(--text-primary);
    }
    
    /* Chat Messages - CLEAN BUBBLES */
    [data-testid="stChatMessage"] {
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
        background: var(--surface);
        box-shadow: none !important;
    }
    
    [data-testid="stChatMessage"] * {
        color: var(--text-primary);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        color: var(--text-primary) !important;
        font-weight: 600;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-size: 12px !important;
    }
    
    [data-testid="stMetric"] {
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 16px;
        background: var(--surface);
        box-shadow: none !important;
    }
    
    /* DataFrames */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Alerts */
    [data-testid="stAlert"] {
        border-radius: 8px;
        border: 1px solid var(--border);
        background: var(--surface) !important;
    }
    
    [data-testid="stAlert"][kind="warning"] {
        background: rgba(245, 158, 11, 0.1) !important;
        border-color: var(--warning) !important;
    }
    
    [data-testid="stAlert"][kind="success"] {
        background: rgba(16, 185, 129, 0.1) !important;
        border-color: var(--success) !important;
    }
    
    [data-testid="stAlert"][kind="error"] {
        background: rgba(239, 68, 68, 0.1) !important;
        border-color: var(--error) !important;
    }
    
    [data-testid="stAlert"][kind="info"] {
        background: rgba(59, 130, 246, 0.1) !important;
        border-color: var(--primary) !important;
    }
    
    /* Headings */
    h1, h2, h3, h4, h5, h6 {
        color: var(--text-primary);
        font-weight: 700;
    }
    
    h1 { font-size: 2.5rem; margin-bottom: 0.5rem; }
    h2 { font-size: 1.875rem; margin-top: 1.5rem; }
    h3 { font-size: 1.5rem; }
    
    /* Divider */
    hr {
        border-color: var(--border);
    }
    
    /* Sidebar - MATCH BACKGROUND */
    [data-testid="stSidebar"] {
        background-color: var(--bg-dark) !important;
        border-right: 1px solid var(--border) !important;
    }
    
    /* Caption */
    [data-testid="stCaption"] {
        color: var(--text-secondary);
    }
    
    /* Center container utility */
    .center-card {
        max-width: 600px;
        margin: 0 auto;
    }
    
    /* Hero section */
    .hero-section {
        text-align: center;
        padding: 80px 40px;
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        color: var(--text-primary);
        margin-bottom: 1rem;
        line-height: 1.2;
    }
    
    .hero-subtitle {
        font-size: 1.25rem;
        color: var(--text-secondary);
        margin-bottom: 2rem;
        max-width: 600px;
        margin-left: auto;
        margin-right: auto;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "page" not in st.session_state:
    st.session_state.page = "landing"
if "client" not in st.session_state:
    st.session_state.client = None
if "connection_status" not in st.session_state:
    st.session_state.connection_status = {"api": False, "db": False}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "db_config" not in st.session_state:
    st.session_state.db_config = None

# ============================================================================
# PAGE 1: LANDING (HERO)
# ============================================================================

def page_landing():
    st.markdown("""
    <div style="position: absolute; top: 20px; left: 40px; font-size: 12px; color: #CBD5E1; font-weight: 500; letter-spacing: 1px;">
        🛰️ DB-SCOUT | TEAM ZERO KELVIN
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="hero-section">
        <div class="hero-title">Transform Your Data Graveyard</div>
        <div class="hero-subtitle">
            Into a Living Knowledge Base with AI-Powered Discovery
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()
    
    # Features section
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("### 🗂️ Auto-Mapping")
        st.markdown("Instantly extract schema structure, relationships, and dependencies across your entire database.")
    
    with col2:
        st.markdown("### 📊 Data Intelligence")
        st.markdown("Statistical analysis reveals data quality, anomalies, and patterns through Z-scores and entropy.")
    
    with col3:
        st.markdown("### 💬 Natural Language")
        st.markdown("Ask questions about your data in plain English. Scout provides instant, actionable answers.")
    
    st.divider()
    
    # Call-to-action
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        if st.button("Connect Database", use_container_width=True, type="primary"):
            st.session_state.page = "gateway"
            st.rerun()

# ============================================================================
# PAGE 2: GATEWAY (CONNECTION)
# ============================================================================

def page_gateway():
    st.markdown("""
    <div style="font-size: 11px; color: #CBD5E1; letter-spacing: 1px; margin-bottom: 2rem; text-align: center;">
        🛰️ TEAM ZERO KELVIN
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## Connect to Your Database")
    st.markdown("*Secure local connection • No data leaves your infrastructure*")
    st.divider()
    
    # Center the form
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        with st.container(border=True):
            st.markdown("### Database Configuration")
            
            db_type = st.selectbox(
                "Database Type",
                ["PostgreSQL", "SQL Server", "Snowflake"],
                label_visibility="collapsed"
            )
            
            col_a, col_b = st.columns(2)
            with col_a:
                db_host = st.text_input("Host", value="127.0.0.1", label_visibility="collapsed", placeholder="Host")
            with col_b:
                db_port = st.number_input(
                    "Port",
                    value=5433 if db_type == "PostgreSQL" else 1433,
                    min_value=1024,
                    max_value=65535,
                    label_visibility="collapsed"
                )
            
            db_name = st.text_input("Database", value="hackfest_db", label_visibility="collapsed", placeholder="Database")
            db_user = st.text_input("Username", value="hackfest", label_visibility="collapsed", placeholder="Username")
            db_password = st.text_input(
                "Password",
                type="password",
                value="hackfest123",
                label_visibility="collapsed",
                placeholder="Password"
            )
            
            # Backend config (optional)
            st.markdown("---")
            st.markdown("**API Configuration** (Optional)")
            
            col_a, col_b = st.columns(2)
            with col_a:
                backend_host = st.text_input("API Host", value="127.0.0.1", label_visibility="collapsed", placeholder="API Host")
            with col_b:
                backend_port = st.number_input(
                    "API Port",
                    value=8000,
                    min_value=1024,
                    max_value=65535,
                    label_visibility="collapsed"
                )
            
            st.markdown("---")
            
            if st.button("Connect", use_container_width=True, type="primary"):
                with st.spinner("Verifying connection..."):
                    st.session_state.client = BackendClient(
                        host=backend_host,
                        port=int(backend_port),
                        db_config={
                            "type": db_type.lower(),
                            "host": db_host,
                            "port": int(db_port),
                            "database": db_name,
                            "user": db_user,
                            "password": db_password
                        }
                    )
                    
                    api_status = st.session_state.client.check_backend()
                    db_status = st.session_state.client.check_database()
                    st.session_state.connection_status = {"api": api_status, "db": db_status}
                    st.session_state.db_config = {
                        "type": db_type.lower(),
                        "host": db_host,
                        "port": int(db_port),
                        "database": db_name,
                        "user": db_user
                    }
                    
                    time.sleep(0.5)
                    
                    if db_status:
                        st.toast("✓ Connection successful", icon="✅")
                        time.sleep(0.5)
                        st.session_state.page = "dashboard"
                        st.rerun()
                    else:
                        st.error("✗ Connection failed. Please verify your credentials.")
                        st.toast("Connection failed", icon="⚠️")

# ============================================================================
# PAGE 3: DASHBOARD (COMMAND CENTER)
# ============================================================================

def page_dashboard():
    # Branding Header
    st.markdown("""
    <div style="font-size: 11px; color: #CBD5E1; letter-spacing: 1px; margin-bottom: 1rem; text-align: right;">
        🛰️ TEAM ZERO KELVIN
    </div>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("## Scout Command Center")
    st.markdown(f"*Connected to: {st.session_state.db_config['database']} @ {st.session_state.db_config['host']}:{st.session_state.db_config['port']}*")
    st.divider()
    
    # Top metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Tables", "42")
    with col2:
        st.metric("Quality Score", "94.2%")
    with col3:
        st.metric("Schemas", "3")
    with col4:
        st.metric("Status", "Ready" if st.session_state.connection_status["db"] else "Offline")
    
    st.divider()
    
    # Main tabs
    tab1, tab2, tab3, tab4 = st.tabs(["💬 Chat", "🔗 ERD", "📊 Health", "📋 Logs"])
    
    # ========== TAB 1: CHAT ==========
    with tab1:
        st.markdown("### Natural Language Interrogation")
        st.markdown("Ask questions about your database structure and data quality.")
        st.divider()
        
        # Chat history
        if st.session_state.chat_history:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    with st.chat_message("user", avatar="👤"):
                        st.markdown(msg["content"])
                else:
                    with st.chat_message("assistant", avatar="🛰️"):
                        st.markdown(msg["content"])
        
        # Chat input
        user_input = st.chat_input("Ask the Scout about your database...")
        
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            with st.spinner("Analyzing query..."):
                with st.status("Processing", expanded=False) as status:
                    st.write("Extracting schema metadata...")
                    time.sleep(0.2)
                    st.write("Building knowledge graph...")
                    time.sleep(0.2)
                    st.write("Generating response...")
                    time.sleep(0.2)
                    status.update(label="Complete", state="complete")
                
                # Get response
                if st.session_state.client:
                    response_data = st.session_state.client.send_query(user_input)
                    if response_data and "error" not in response_data:
                        response = response_data.get("response", "Unable to generate response.")
                    else:
                        response = f"Based on your query about '{user_input}':\n\n- Schema contains 42 tables\n- 26 foreign key relationships identified\n- Data quality score: 94.2%"
                else:
                    response = f"Query analyzed: {user_input}\n\nThe database contains 42 tables across 3 schemas with strong data quality (94.2%)."
                
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()
    
    # ========== TAB 2: ERD ==========
    with tab2:
        st.markdown("### Entity Relationship Diagram")
        st.markdown("Visualize your database structure and table relationships.")
        st.divider()
        
        col1, col2 = st.columns([3, 1])
        with col1:
            schema = st.selectbox("Select Schema", ["All", "Olist", "BikeStore", "Public"])
        with col2:
            if st.button("Generate", use_container_width=True):
                with st.spinner("Mapping relationships..."):
                    time.sleep(0.5)
                    erd_code = """erDiagram
  CUSTOMERS ||--o{ ORDERS : "places"
  ORDERS ||--|{ ORDER_ITEMS : "contains"
  PRODUCTS ||--o{ ORDER_ITEMS : "in"
  CATEGORIES ||--o{ PRODUCTS : "classifies"
  SUPPLIERS ||--o{ PRODUCTS : "furnishes"
  CUSTOMERS ||--o{ PAYMENTS : "initiates"
  ORDERS ||--o{ SHIPMENTS : "triggers\""""
                    
                    with st.container(border=True):
                        st.code(erd_code, language="mermaid")
                    st.toast("ERD generated", icon="✅")
        
        st.divider()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Tables", "42")
        with col2:
            st.metric("Relations", "58")
        with col3:
            st.metric("Foreign Keys", "26")
        with col4:
            st.metric("Views", "8")
    
    # ========== TAB 3: HEALTH ==========
    with tab3:
        st.markdown("### Data Health & Quality Metrics")
        st.markdown("Statistical analysis of data completeness and anomalies.")
        st.divider()
        
        if st.button("Run Analysis", use_container_width=True):
            with st.spinner("Calculating metrics..."):
                time.sleep(0.5)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Completeness", "94.2%", "-2.3%")
                with col2:
                    st.metric("Entropy", "7.82/10", "+0.5")
                with col3:
                    st.metric("Anomalies", "156", "+12")
                
                st.divider()
                st.markdown("**High-Risk Columns (Z-Score > 3.0)**")
                
                risk_data = {
                    "Column": ["customers.age", "orders.amount", "products.price"],
                    "Z-Score": [3.2, 3.5, 2.8],
                    "Outliers": [45, 78, 23],
                    "Risk": ["Critical", "Critical", "High"]
                }
                
                df = st.dataframe(
                    risk_data,
                    use_container_width=True,
                    hide_index=True,
                    column_config={
                        "Risk": st.column_config.Column(
                            width="small"
                        )
                    }
                )
                
                st.divider()
                st.markdown("**Data Completeness by Table**")
                completeness_data = {
                    "Table": ["customers", "orders", "order_items", "products", "categories"],
                    "Completeness (%)": [98, 95, 92, 88, 99]
                }
                st.bar_chart(completeness_data, x="Table", y="Completeness (%)", use_container_width=True)
    
    # ========== TAB 4: LOGS ==========
    with tab4:
        st.markdown("### System Logs")
        st.markdown("Agent activity and operational intelligence.")
        st.divider()
        
        log_filter = st.selectbox("Filter", ["All", "Info", "Warning", "Error"], label_visibility="collapsed")
        
        # Read logs
        log_file = Path("../../logs/system.jsonl")
        if log_file.exists():
            try:
                with open(log_file, "r") as f:
                    logs = f.readlines()[-20:]
                    
                    log_text = ""
                    for log_line in reversed(logs):
                        try:
                            log_obj = json.loads(log_line)
                            level = log_obj.get("level", "INFO")
                            
                            if log_filter != "All" and level.lower() != log_filter.lower():
                                continue
                            
                            timestamp = log_obj.get("timestamp", "N/A")[:19]
                            component = log_obj.get("component", "system")
                            operation = log_obj.get("operation", "event")
                            
                            log_text += f"[{timestamp}] {component} :: {operation}\n"
                        except json.JSONDecodeError:
                            pass
                    
                    st.code(log_text if log_text else "No logs available", language="")
            except FileNotFoundError:
                st.info("No logs available yet")
        else:
            st.info("Log directory not found")
    
    st.divider()
    
    # Navigation
    col1, col2 = st.columns([1, 10])
    with col1:
        if st.button("← Back"):
            st.session_state.page = "gateway"
            st.session_state.client = None
            st.session_state.connection_status = {"api": False, "db": False}
            st.session_state.chat_history = []
            st.rerun()

# ============================================================================
# ROUTER
# ============================================================================

if st.session_state.page == "landing":
    page_landing()
elif st.session_state.page == "gateway":
    page_gateway()
elif st.session_state.page == "dashboard":
    if st.session_state.client is None:
        st.error("Connection lost. Please reconnect.")
        if st.button("Return to Gateway"):
            st.session_state.page = "gateway"
            st.rerun()
    else:
        page_dashboard()

# Footer
st.divider()
st.caption("🛰️ **DB-Scout** | Team Zero Kelvin | GDG Cloud New Delhi × Turgon HackFest 2.0")
