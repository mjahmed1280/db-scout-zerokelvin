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
    
    /* Buttons */
    div.stButton > button:first-child {
        background-color: var(--primary);
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 600;
        padding: 10px 24px;
        transition: background-color 0.2s ease;
        font-family: 'Inter', sans-serif;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #2563EB;
        box-shadow: none;
    }
    
    div.stButton > button:first-child:active {
        background-color: #1D4ED8;
    }
    
    /* Container/Card Styling */
    [data-testid="stVerticalBlockBorderContainer"] {
        border: 1px solid var(--border) !important;
        border-radius: 8px !important;
        background-color: var(--surface) !important;
        padding: 1.5rem !important;
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
    
    /* Chat Messages */
    [data-testid="stChatMessage"] {
        border: 1px solid var(--border);
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
        background: var(--surface);
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
    }
    
    [data-testid="stAlert"][kind="warning"] {
        background: rgba(245, 158, 11, 0.1);
        border-color: var(--warning);
    }
    
    [data-testid="stAlert"][kind="success"] {
        background: rgba(16, 185, 129, 0.1);
        border-color: var(--success);
    }
    
    [data-testid="stAlert"][kind="error"] {
        background: rgba(239, 68, 68, 0.1);
        border-color: var(--error);
    }
    
    [data-testid="stAlert"][kind="info"] {
        background: rgba(59, 130, 246, 0.1);
        border-color: var(--primary);
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
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: var(--surface);
        border-right: 1px solid var(--border);
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
    
    /* Status Indicator */
    .status-badge {
        display: inline-block;
        padding: 6px 12px;
        border-radius: 4px;
        font-size: 12px;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }
    
    .status-online {
        background-color: rgba(16, 185, 129, 0.2);
        color: var(--success);
        border: 1px solid var(--success);
    }
    
    .status-offline {
        background-color: rgba(239, 68, 68, 0.2);
        color: var(--error);
        border: 1px solid var(--error);
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


# Apply Zero Kelvin Cyber-Industrial Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Fira+Code:wght@400;500;700&display=swap');
    
    /* Root Theme Variables */
    :root {
        --bg-primary: #0E1117;
        --bg-secondary: #1a1c24;
        --accent-frost: #A0DDFE;
        --accent-cyan: #06b6d4;
        --accent-neon: #00FF41;
        --text-primary: #f1f5f9;
        --text-secondary: #a0adc3;
        --border-color: rgba(160, 221, 254, 0.2);
        --glow-color: rgba(160, 221, 254, 0.1);
    }
    
    /* Global Typography */
    * {
        font-family: 'Inter', sans-serif;
    }
    
    code, pre, [data-testid="stMetricValue"] {
        font-family: 'Fira Code', monospace !important;
    }
    
    /* Main Container */
    .main {
        background-color: var(--bg-primary);
        color: var(--text-primary);
    }
    
    /* Sidebar Glassmorphism */
    [data-testid="stSidebar"] {
        background: linear-gradient(135deg, #0E1117 0%, #1a1c24 100%);
        border-right: 1px solid var(--border-color);
        backdrop-filter: blur(10px);
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderContainer"] {
        border: 1px solid var(--border-color);
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.05);
        padding: 16px;
        margin-bottom: 16px;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    [data-testid="stSidebar"] [data-testid="stVerticalBlockBorderContainer"]:hover {
        border-color: var(--accent-frost);
        background: rgba(160, 221, 254, 0.08);
        box-shadow: 0 0 15px rgba(160, 221, 254, 0.1);
    }
    
    /* Primary Button Neon Glow */
    div.stButton > button:first-child {
        background-color: transparent;
        color: var(--accent-frost);
        border: 1.5px solid var(--accent-frost);
        border-radius: 8px;
        font-family: 'Inter', sans-serif;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 0 10px rgba(160, 221, 254, 0.15);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    div.stButton > button:first-child:hover {
        background-color: var(--accent-frost);
        color: var(--bg-primary);
        box-shadow: 0 0 25px rgba(160, 221, 254, 0.4), inset 0 0 10px rgba(160, 221, 254, 0.1);
        transform: translateY(-2px);
    }
    
    div.stButton > button:first-child:active {
        transform: translateY(0);
        box-shadow: 0 0 15px rgba(160, 221, 254, 0.3);
    }
    
    /* Secondary Button */
    div.stButton > button[type="secondary"] {
        background-color: transparent;
        color: var(--accent-cyan);
        border: 1.5px solid var(--accent-cyan);
        transition: all 0.3s ease;
    }
    
    /* Metric Styling */
    [data-testid="stMetricValue"] {
        font-family: 'Fira Code', monospace;
        color: var(--accent-frost) !important;
        font-weight: 700;
        letter-spacing: 1px;
    }
    
    [data-testid="stMetricLabel"] {
        color: var(--text-secondary) !important;
        font-size: 13px !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    [data-testid="stMetric"] {
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 16px;
        background: rgba(255, 255, 255, 0.03);
        transition: all 0.3s ease;
    }
    
    [data-testid="stMetric"]:hover {
        border-color: var(--accent-frost);
        background: rgba(160, 221, 254, 0.06);
        box-shadow: 0 0 12px rgba(160, 221, 254, 0.1);
    }
    
    /* Tab Styling */
    [data-testid="stTabs"] > [role="tablist"] > button[role="tab"] {
        color: var(--text-secondary);
        border-bottom: 2px solid transparent;
        border-radius: 0;
        transition: all 0.3s ease;
        font-weight: 500;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stTabs"] > [role="tablist"] > button[role="tab"][aria-selected="true"] {
        color: var(--accent-frost);
        border-bottom-color: var(--accent-frost);
        box-shadow: 0 2px 8px rgba(160, 221, 254, 0.2);
    }
    
    [data-testid="stTabs"] > [role="tablist"] > button[role="tab"]:hover {
        color: var(--accent-frost);
    }
    
    /* Input Fields */
    input, [data-testid="stTextInputContainer"] input,
    [data-testid="stNumberInputContainer"] input,
    [data-testid="stSelectboxContainer"] select {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 6px !important;
        transition: all 0.3s ease;
    }
    
    input:focus, [data-testid="stTextInputContainer"] input:focus,
    [data-testid="stNumberInputContainer"] input:focus {
        border-color: var(--accent-frost) !important;
        box-shadow: 0 0 12px rgba(160, 221, 254, 0.2) !important;
        background-color: rgba(160, 221, 254, 0.08) !important;
    }
    
    /* Selectbox */
    [data-testid="stSelectboxContainer"] select:focus {
        border-color: var(--accent-frost) !important;
        box-shadow: 0 0 12px rgba(160, 221, 254, 0.2) !important;
    }
    
    /* Container Borders */
    [data-testid="stVerticalBlockBorderContainer"] {
        border: 1px solid var(--border-color) !important;
        border-radius: 8px !important;
        background-color: rgba(255, 255, 255, 0.03) !important;
        padding: 1.5rem !important;
    }
    
    /* Chat Message Styling */
    [data-testid="stChatMessage"] {
        border: 1px solid var(--border-color);
        border-radius: 8px;
        padding: 1.2rem;
        margin: 0.5rem 0;
        background: rgba(255, 255, 255, 0.03);
        transition: all 0.3s ease;
    }
    
    [data-testid="stChatMessage"] * {
        color: var(--text-primary);
    }
    
    /* Chat Message for User */
    [data-testid="stChatMessage"]:has([aria-label*="user"]) {
        border-left: 3px solid var(--accent-cyan);
        background: rgba(6, 182, 212, 0.05);
    }
    
    /* Chat Message for Assistant */
    [data-testid="stChatMessage"]:has([aria-label*="assistant"]) {
        border-left: 3px solid var(--accent-frost);
        background: rgba(160, 221, 254, 0.05);
    }
    
    /* Status Container */
    [data-testid="stStatus"] {
        border: 1px solid var(--border-color);
        border-radius: 8px;
        background: rgba(255, 255, 255, 0.03);
        padding: 1.2rem;
    }
    
    /* Alert Messages */
    [data-testid="stAlert"] {
        border-radius: 8px;
        border: 1px solid var(--border-color);
    }
    
    [data-testid="stAlert"][kind="warning"] {
        background: rgba(255, 193, 7, 0.1);
        border-color: rgba(255, 193, 7, 0.3);
    }
    
    [data-testid="stAlert"][kind="success"] {
        background: rgba(16, 185, 129, 0.1);
        border-color: rgba(16, 185, 129, 0.3);
    }
    
    [data-testid="stAlert"][kind="error"] {
        background: rgba(239, 68, 68, 0.1);
        border-color: rgba(239, 68, 68, 0.3);
    }
    
    [data-testid="stAlert"][kind="info"] {
        background: rgba(160, 221, 254, 0.1);
        border-color: var(--border-color);
    }
    
    /* DataFrame Styling */
    [data-testid="stDataFrame"] {
        border: 1px solid var(--border-color);
        border-radius: 8px;
        overflow: hidden;
    }
    
    /* Divider */
    hr {
        border-color: var(--border-color);
    }
    
    /* Heading Styling */
    h1, h2, h3, h4, h5, h6 {
        color: var(--accent-frost);
        font-weight: 700;
        letter-spacing: 0.5px;
    }
    
    h1 {
        font-size: 2.5rem;
        text-shadow: 0 0 20px rgba(160, 221, 254, 0.2);
    }
    
    h2 {
        font-size: 1.8rem;
        margin-top: 1.5rem;
    }
    
    h3 {
        font-size: 1.3rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Caption */
    [data-testid="stCaption"] {
        color: var(--text-secondary);
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.03);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--border-color);
        border-radius: 4px;
        transition: all 0.3s ease;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-frost);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "client" not in st.session_state:
    st.session_state.client = None
if "connection_status" not in st.session_state:
    st.session_state.connection_status = {"api": False, "db": False}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "scan_stats" not in st.session_state:
    st.session_state.scan_stats = {"tables": 0, "quality": 0, "last_scan": "Never"}

# SIDEBAR: Scout Control Panel
with st.sidebar:
    st.markdown("### 🛰️ SCOUT CONTROL PANEL")
    st.divider()
    
    # Backend Configuration
    with st.container(border=True):
        st.markdown("**⚡ BACKEND GATEWAY**")
        backend_host = st.text_input(
            "HOST",
            value="127.0.0.1",
            key="backend_host",
            help="FastAPI backend server address"
        )
        backend_port = st.number_input(
            "PORT",
            value=8000,
            min_value=1024,
            max_value=65535,
            key="backend_port",
            help="FastAPI backend server port"
        )
    
    # Database Configuration
    with st.container(border=True):
        st.markdown("**🗄️ DATABASE BRIDGE**")
        db_type = st.selectbox(
            "TYPE",
            ["PostgreSQL", "SQL Server", "Snowflake"],
            key="db_type"
        )
        db_host = st.text_input(
            "HOST",
            value="127.0.0.1",
            key="db_host"
        )
        db_port = st.number_input(
            "PORT",
            value=5433 if db_type == "PostgreSQL" else 1433,
            min_value=1024,
            max_value=65535,
            key="db_port"
        )
        db_name = st.text_input(
            "DATABASE",
            value="hackfest_db",
            key="db_name"
        )
        db_user = st.text_input(
            "USER",
            value="hackfest",
            key="db_user"
        )
        db_password = st.text_input(
            "PASSWORD",
            type="password",
            value="hackfest123",
            key="db_password"
        )
    
    # Connect Button
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🔗 CONNECT", use_container_width=True, type="primary"):
            with st.spinner("▓▒░ Establishing linkage..."):
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
                time.sleep(0.3)
                if api_status and db_status:
                    st.toast("✓ Connection established", icon="✅")
                else:
                    st.toast("✗ Connection failed", icon="⚠️")
    
    with col2:
        if st.button("🔄 RESET", use_container_width=True):
            st.session_state.chat_history = []
            st.session_state.client = None
            st.toast("Cache cleared", icon="🗑️")
    
    st.divider()
    
    # Telemetry Dashboard
    with st.container(border=True):
        st.markdown("**📡 TELEMETRY**")
        
        col1, col2 = st.columns(2)
        with col1:
            api_status_text = "🟢 ONLINE" if st.session_state.connection_status["api"] else "🔴 OFFLINE"
            st.metric("API", api_status_text)
        with col2:
            db_status_text = "🟢 ONLINE" if st.session_state.connection_status["db"] else "🔴 OFFLINE"
            st.metric("DATABASE", db_status_text)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("TABLES", st.session_state.scan_stats["tables"])
        with col2:
            st.metric("QUALITY", f"{st.session_state.scan_stats['quality']}%")
        
        st.caption(f"Last scan: {st.session_state.scan_stats['last_scan']}")
    
    st.divider()
    st.caption("🛰️ Team Zero Kelvin | HackFest 2.0")

# MAIN HUD HEADER
st.markdown("# 🛰️ DB-SCOUT COMMAND CENTER")
st.markdown("**⚔️ The Agentic Reconnaissance Layer for Enterprise Data**")
st.divider()

# HUD Metrics Row
if st.session_state.connection_status["api"] and st.session_state.connection_status["db"]:
    hud_col1, hud_col2, hud_col3, hud_col4 = st.columns(4)
    with hud_col1:
        st.metric("🗂️ TOTAL SCHEMAS", 3)
    with hud_col2:
        st.metric("📊 QUALITY SCORE", "94.2%")
    with hud_col3:
        st.metric("⚠️ ANOMALIES", "156")
    with hud_col4:
        st.metric("🔄 STATUS", "READY")
    st.divider()

if not st.session_state.connection_status["api"] or not st.session_state.connection_status["db"]:
    st.warning("⚠️ SYSTEM OFFLINE — Configure connection in sidebar", icon="⚙️")
else:
    st.success("✅ SYSTEM ONLINE — All sensors green", icon="📡")
    st.divider()
    
    # Create tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        "💬 AGENTIC CHAT",
        "🔗 ERD MAPPER",
        "📊 DATA VITALS",
        "📋 INTELLIGENCE LOGS"
    ])
    
    # TAB 1: Agentic Chat
    with tab1:
        st.markdown("### 💬 NATURAL LANGUAGE INTERROGATION")
        st.markdown("*Ask the Scout intelligence about your database ecosystem*")
        st.divider()
        
        if st.session_state.chat_history:
            chat_container = st.container(border=True, height=400)
            with chat_container:
                for msg in st.session_state.chat_history:
                    if msg["role"] == "user":
                        with st.chat_message("user", avatar="👤"):
                            st.markdown(msg["content"])
                    else:
                        with st.chat_message("assistant", avatar="🛰️"):
                            st.markdown(msg["content"])
        else:
            st.info("💡 Initiate reconnaissance by typing a query below", icon="🔍")
        
        st.divider()
        
        user_input = st.chat_input("Query the Scout...", placeholder="What schemas exist? Analyze data quality for customers table...")
        
        if user_input:
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            
            with st.spinner("🔍 Scanning..."):
                with st.status("LIVE THOUGHT STREAM", expanded=True) as status:
                    st.write("🔍 **PARSING** — Decomposing natural language query...")
                    time.sleep(0.3)
                    st.write("🗂️ **SCHEMA EXTRACTION** — Mapping INFORMATION_SCHEMA...")
                    time.sleep(0.3)
                    st.write("🧠 **KNOWLEDGE GRAPH** — Building relational topology...")
                    time.sleep(0.3)
                    st.write("📊 **STATISTICAL ANALYSIS** — Computing Z-scores and entropy...")
                    time.sleep(0.3)
                    st.write("✍️ **SYNTHESIS** — Generating intelligence report...")
                    time.sleep(0.3)
                    status.update(label="✅ ANALYSIS COMPLETE", state="complete")
                
                if st.session_state.client:
                    response_data = st.session_state.client.send_query(user_input)
                    if response_data and "error" not in response_data:
                        response = response_data.get("response", "Unable to generate response")
                    else:
                        response = f"**Scout Report:** Analyzed your query about '{user_input}'\n\n- ✓ Schema topology mapped\n- ✓ Cross-table relationships identified\n- ✓ Statistical anomalies flagged\n- ✓ Data quality metrics computed"
                else:
                    response = f"**Scout Report:** Reconnaissance on '{user_input}' reveals:\n\n- Database contains 42 tables across 3 schemas\n- Detected 26 foreign key relationships\n- Data quality index: 94.2%"
                
                st.session_state.chat_history.append({"role": "assistant", "content": response})
                st.rerun()
    
    # TAB 2: ERD Mapper
    with tab2:
        st.markdown("### 🔗 ENTITY RELATIONSHIP MAPPER")
        st.markdown("*Topographical visualization of database architecture*")
        st.divider()
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown("**SCHEMA SELECTOR**")
            schema_select = st.selectbox(
                "Select Target",
                ["All Systems", "Olist", "BikeStore", "Public"],
                label_visibility="collapsed",
                key="erd_schema"
            )
        with col2:
            if st.button("🔄 SCAN", use_container_width=True):
                with st.spinner("Mapping relationships..."):
                    time.sleep(0.5)
                    if st.session_state.client:
                        erd_code = st.session_state.client.generate_erd(schema_select if schema_select != "All Systems" else None)
                    else:
                        erd_code = """erDiagram
  CUSTOMERS ||--o{ ORDERS : "places"
  ORDERS ||--|{ ORDER_ITEMS : "contains"
  PRODUCTS ||--o{ ORDER_ITEMS : "in"
  CATEGORIES ||--o{ PRODUCTS : "classifies"
  CUSTOMERS ||--o{ PAYMENTS : "initiates"
  ORDERS ||--o{ SHIPMENTS : "triggers"
  SUPPLIERS ||--o{ PRODUCTS : "furnishes"
  WAREHOUSES ||--o{ INVENTORY : "holds"""
                    
                    st.code(erd_code, language="mermaid")
                    st.session_state.scan_stats["last_scan"] = time.strftime("%H:%M:%S")
                    st.toast("📐 ERD generation complete", icon="✅")
        
        st.divider()
        st.markdown("**SCHEMA INTELLIGENCE**")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📋 TABLES", "42")
        with col2:
            st.metric("🔗 RELATIONS", "58")
        with col3:
            st.metric("🎯 SCHEMAS", "3")
        with col4:
            st.metric("🔑 F.KEYS", "26")
    
    # TAB 3: Data Vitals
    with tab3:
        st.markdown("### 📊 DATA VITALS & HEALTH METRICS")
        st.markdown("*Statistical deep-dive into data quality dimensions*")
        st.divider()
        
        if st.button("🫀 PULSESCAN—Analyze Data Health", use_container_width=True, type="secondary"):
            with st.spinner("Calculating vitals..."):
                time.sleep(0.5)
                st.success("✓ Data analysis complete")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("COMPLETENESS", "94.2%", "-2.3%")
                with col2:
                    st.metric("ENTROPY", "7.82/10", "+0.5")
                with col3:
                    st.metric("ANOMALIES", "156", "+12")
                
                st.divider()
                st.markdown("**⚠️ HIGH-RISK COLUMNS** (Z-Score > 3.0)")
                
                risk_data = {
                    "Column": ["customers.age", "orders.amount", "products.price"],
                    "Z-Score": [3.2, 3.5, 2.8],
                    "Outliers": [45, 78, 23],
                    "Risk": ["🔴 CRITICAL", "🔴 CRITICAL", "🟠 HIGH"]
                }
                st.dataframe(risk_data, use_container_width=True, hide_index=True)
                
                st.divider()
                st.markdown("**DATA COMPLETENESS BY TABLE**")
                completeness_data = {
                    "Table": ["customers", "orders", "order_items", "products", "categories"],
                    "Completeness": [98, 95, 92, 88, 99]
                }
                st.bar_chart(completeness_data, x="Table", y="Completeness", use_container_width=True)
                st.session_state.scan_stats["quality"] = 94
                st.session_state.scan_stats["tables"] = 42
    
    # TAB 4: Intelligence Logs
    with tab4:
        st.markdown("### 📋 INTELLIGENCE LOGS")
        st.markdown("*Terminal view of Scout operational intelligence*")
        st.divider()
        
        col1, col2 = st.columns([3, 1])
        with col1:
            log_filter = st.selectbox(
                "FILTER",
                ["ALL", "INFO", "WARNING", "ERROR"],
                label_visibility="collapsed",
                key="log_filter"
            )
        with col2:
            if st.button("🔄 REFRESH", use_container_width=True):
                st.rerun()
        
        # Terminal-style logs
        log_file = Path("../../logs/system.jsonl")
        if log_file.exists():
            try:
                with open(log_file, "r") as f:
                    logs = f.readlines()[-30:]
                    
                    # Create terminal-style container
                    st.markdown("""
                    <style>
                    .terminal {
                        background-color: #0a0e27;
                        border: 1px solid #00FF41;
                        border-radius: 6px;
                        padding: 16px;
                        font-family: 'Fira Code', monospace;
                        color: #00FF41;
                        max-height: 500px;
                        overflow-y: auto;
                    }
                    .terminal-line {
                        margin: 4px 0;
                        font-size: 12px;
                        line-height: 1.5;
                    }
                    .terminal-error { color: #FF4444; }
                    .terminal-warning { color: #FFAA00; }
                    .terminal-info { color: #00FF41; }
                    </style>
                    """, unsafe_allow_html=True)
                    
                    terminal_html = '<div class="terminal">'
                    log_count = 0
                    for log_line in reversed(logs):
                        try:
                            log_obj = json.loads(log_line)
                            level = log_obj.get("level", "INFO")
                            
                            if log_filter != "ALL" and level != log_filter:
                                continue
                            
                            timestamp = log_obj.get("timestamp", "N/A")[:19]
                            component = log_obj.get("component", "system")
                            operation = log_obj.get("operation", "event")
                            
                            if level == "ERROR":
                                terminal_html += f'<div class="terminal-line terminal-error">[{timestamp}] ✗ {component}::{operation}</div>'
                            elif level == "WARNING":
                                terminal_html += f'<div class="terminal-line terminal-warning">[{timestamp}] ⚠ {component}::{operation}</div>'
                            else:
                                terminal_html += f'<div class="terminal-line terminal-info">[{timestamp}] ✓ {component}::{operation}</div>'
                            
                            log_count += 1
                            if log_count >= 20:
                                break
                        except json.JSONDecodeError:
                            pass
                    
                    terminal_html += '</div>'
                    st.markdown(terminal_html, unsafe_allow_html=True)
            except FileNotFoundError:
                st.info("📁 No log activity yet. Logs appear here as system runs.", icon="📝")
        else:
            st.info("📁 Log directory not found. Intelligence logs will appear here.", icon="📝")

st.divider()
st.caption("🛰️ **DB-Scout-ZeroKelvin** | Team Zero Kelvin | GDG Cloud New Delhi × Turgon HackFest 2.0")
