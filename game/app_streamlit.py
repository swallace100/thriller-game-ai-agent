import streamlit as st
import nest_asyncio
from dotenv import load_dotenv

load_dotenv(dotenv_path="../resources/openaiApiKey.env")
nest_asyncio.apply()

try:
    from thriller_module import respond_narrator
    deps_ok = True
except ModuleNotFoundError:
    deps_ok = False

st.set_page_config(page_title="Thriller Game")
st.title("Thriller Game w/ Narrator Agent")

if not deps_ok:
    st.warning("Dependency missing: 'openai-agents' (module 'agents'). Run: pip install openai-agents")
else:
    if "chat" not in st.session_state:
        st.session_state.chat = []
    # Display history
    for role, content in st.session_state.chat:
        with st.chat_message(role):
            st.markdown(content)
    # Input
    prompt = st.chat_input("Type your action...")
    if prompt:
        st.session_state.chat.append(("user", prompt))
        with st.chat_message("user"):
            st.markdown(prompt)
        reply = respond_narrator(prompt)
        st.session_state.chat.append(("assistant", reply))
        with st.chat_message("assistant"):
            st.markdown(reply)
