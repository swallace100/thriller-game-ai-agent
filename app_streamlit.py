"""
Eternal Hunt: AI Agent Powered Game — Streamlit Web App
"""

import os

import streamlit as st
from dotenv import load_dotenv

from game.config import (
    API_KEY_PATH,
    APP_DESC,
    APP_NAME,
    APP_VERSION,
    EXAMPLE_COMMANDS,
)
from game.content import NARRATOR_INTRO
from game.router import Router
from game.ui_shared import (
    STREAMLIT_CSS,
    TIP_TEXT,
    card_html,
    footer_html,
    has_api_key,
    header_html,
)

# Load environment variables before importing game modules
if os.path.exists(".env"):
    load_dotenv()
elif os.path.exists(API_KEY_PATH):
    load_dotenv(dotenv_path=API_KEY_PATH)

# Single router instance per process
_ROUTER = Router()


def css():
    st.markdown(f"<style>{STREAMLIT_CSS}</style>", unsafe_allow_html=True)


def sidebar():
    with st.sidebar:
        st.markdown(f"### {APP_NAME}")
        st.caption(APP_DESC)
        st.markdown(f"**Version:** v{APP_VERSION}")
        st.markdown(f"**API key loaded:** {'✅' if has_api_key() else '❌'}")

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
        for i, ex in enumerate(EXAMPLE_COMMANDS):
            if ex_cols[i % 2].button(ex, key=f"ex_{i}", use_container_width=True):
                st.session_state["_pending_prompt"] = ex
                st.rerun()


def header():
    st.markdown(header_html(APP_NAME, APP_VERSION), unsafe_allow_html=True)
    st.markdown(card_html(APP_DESC, TIP_TEXT), unsafe_allow_html=True)


def render_history():
    for role, content in st.session_state.chat:
        with st.chat_message(role):
            st.markdown(content)


def handle_submit(text: str):
    st.session_state.chat.append(("user", text))
    with st.chat_message("user"):
        st.markdown(text)

    try:
        reply = _ROUTER.handle(text, st.session_state.chat)
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

    # 🔽 Seed intro once if chat is empty
    if not st.session_state.chat:
        st.session_state.chat.append(("assistant", NARRATOR_INTRO))

    header()

    if not _ROUTER.ready:
        st.warning(
            "⚠️ Dependency missing or not importable: `game.engine.respond_narrator`. "
            "Ensure the agents framework is installed and imports succeed."
        )

    render_history()

    pending = st.session_state.get("_pending_prompt")
    if pending:
        st.session_state["_pending_prompt"] = None
        handle_submit(pending)
    else:
        user_text = st.chat_input("Type your action...")
        if user_text:
            handle_submit(user_text)

    st.markdown(footer_html(APP_NAME), unsafe_allow_html=True)


if __name__ == "__main__":
    main()
