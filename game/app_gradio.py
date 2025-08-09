# gradio app for the Thriller Game Agent (cleaned)
import os, asyncio, nest_asyncio
from dotenv import load_dotenv
from fastapi.responses import FileResponse
import gradio as gr

load_dotenv(dotenv_path="../resources/openaiApiKey.env")
nest_asyncio.apply()

try:
    from thriller_module import respond_narrator
except ModuleNotFoundError as e:
    # Provide a friendly message if dependencies are missing
    def respond_narrator(_msg):
        return "Dependency missing: 'openai-agents' (module 'agents'). Please run: pip install openai-agents"
    
def chat_respond(message, history):
    return respond_narrator(message)

with gr.Blocks(title="Thriller Game") as demo:
    gr.Markdown("# Thriller Game w/ Narrator Agent")
    gr.Markdown("Type your actions or questions below to play.")
    chat = gr.ChatInterface(
        fn=chat_respond,
        type="messages",
        textbox=gr.Textbox(placeholder="e.g., 'Look around the room'")
    )

if __name__ == "__main__":
    demo.launch()
