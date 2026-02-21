import streamlit as st
import json
import datetime

# Setup Logger (Simple implementation for prototype)
def log_action(action, details):
    entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "component": "frontend.main",
        "operation": action,
        "details": details
    }
    # In production, ensure thread safety or use a logging library
    with open("../logs/frontend.jsonl", "a") as f:
        f.write(json.dumps(entry) + "")

st.set_page_config(page_title="Intelligent Data Dictionary", layout="wide")

st.title("Intelligent Data Dictionary Agent")
st.sidebar.header("Configuration")

# Placeholder for future connection settings
db_type = st.sidebar.selectbox("Database Type", ["PostgreSQL", "Snowflake", "SQL Server"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about your data..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    log_action("user_query", {"query": prompt})

    # Placeholder response logic
    response = f"I received your query about {db_type}: '{prompt}'. (Backend connection pending)"
    
    with st.chat_message("assistant"):
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
