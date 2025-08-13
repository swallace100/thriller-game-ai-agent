"""
Thriller Game — Streamlit Web App
A cleaner, production-leaning structure (functions, constants, minimal comments).
"""
import os
import datetime
import nest_asyncio
import streamlit as st
from dotenv import load_dotenv

# ----- configuration -----
APP_NAME = "Thriller Game"
APP_DESC = "A near-future text thriller powered by a Narrator Agent."
APP_VERSION = "0.1.0"
ENV_PATH = "../resources/openaiApiKey.env"

# env + asyncio
load_dotenv(dotenv_path=ENV_PATH)
nest_asyncio.apply()

# core deps
try:
    from game.thriller_module import respond_narrator
    DEPS_OK = True
except ModuleNotFoundError:
    DEPS_OK = False

# ----- ui helpers -----
def css():
    st.markdown(
        """
        <style>
        .main .block-container { max-width: 900px; }
        .app-header { display:flex; align-items:center; gap:12px; margin-top:8px; }
        .app-title { font-weight:800; font-size:1.6rem; letter-spacing:0.2px; }
        .app-meta { color:#6b7280; font-size:0.95rem; }
        .tip { color:#6b7280; font-size:0.9rem; margin-top:-6px; }
        .footer { color:#6b7280; font-size:0.85rem; text-align:center; margin-top:12px; }
        </style>
        """,
        unsafe_allow_html=True,
    )

def sidebar():
    with st.sidebar:
        st.markdown(f"### {APP_NAME}")
        st.caption(APP_DESC)
        st.markdown(f"**Version:** v{APP_VERSION}")
        st.markdown(f"**API key loaded:** {'✅' if os.getenv('OPENAI_API_KEY') else '❌'}")
        col_a, col_b = st.columns(2)
        with col_a:
            if st.button("Clear chat", use_container_width=True):
                st.session_state.chat = []
                st.rerun()
        with col_b:
            st.toggle("Auto-scroll", value=True, key="auto_scroll")
        st.markdown("---")
        st.markdown("##### Examples")
        ex_cols = st.columns(2)
        examples = ["Look around", "Inventory", "Open the door", "Run outside"]
        for i, ex in enumerate(examples):
            if ex_cols[i % 2].button(ex, key=f"ex_{i}", use_container_width=True):
                st.session_state["_pending_prompt"] = ex
                st.rerun()

def header():
    st.markdown(
        f"""
        <div class="app-header">
          <div class="app-title">{APP_NAME}</div>
          <div class="app-meta">v{APP_VERSION}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.write(APP_DESC)
    st.markdown('<div class="tip">Try “Look around”, “Inventory”, “Open the door”.</div>', unsafe_allow_html=True)

def render_history():
    for role, content in st.session_state.chat:
        with st.chat_message(role):
            st.markdown(content)

def handle_submit(text: str):
    st.session_state.chat.append(("user", text))
    with st.chat_message("user"):
        st.markdown(text)
    try:
        reply = respond_narrator(text)
    except Exception as e:
        reply = f"⚠️ Error: {e!s}"
    st.session_state.chat.append(("assistant", reply))
    with st.chat_message("assistant"):
        st.markdown(reply)
    if st.session_state.get("auto_scroll", True):
        st.empty()

def main():
    st.set_page_config(page_title=APP_NAME, page_icon="🎭", layout="centered")
    css()
    sidebar()
    if "chat" not in st.session_state:
        st.session_state.chat = []
    if "_pending_prompt" not in st.session_state:
        st.session_state["_pending_prompt"] = None

    header()
    if not DEPS_OK:
        st.warning("Dependency missing: `openai-agents` (module `agents`). Run: `pip install openai-agents`", icon="⚠️")

    render_history()

    pending = st.session_state.get("_pending_prompt")
    if pending:
        st.session_state["_pending_prompt"] = None
        handle_submit(pending)
    else:
        user_text = st.chat_input("Type your action...")
        if user_text and DEPS_OK:
            handle_submit(user_text)

    st.markdown(f"<div class='footer'>© {datetime.datetime.now().year} — {APP_NAME}</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
