import streamlit as st


def initialize_session_state():
    """Ensure all required session state variables are initialized."""
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = set()
    if "vectorstore" not in st.session_state:
        st.session_state.vectorstore = None
    if "llm" not in st.session_state:
        st.session_state.llm = None
    if "memory" not in st.session_state:
        st.session_state.memory = None
    if "chain" not in st.session_state:
        st.session_state.chain = None


def verify_session_state():
    required_keys = ["chat_history", "vectorstore", "llm", "memory", "chain"]
    for key in required_keys:
        if key not in st.session_state or st.session_state[key] is None:
            st.error(f"Session state key '{key}' is not initialized.")
