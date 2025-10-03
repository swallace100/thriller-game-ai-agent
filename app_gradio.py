"""
Eternal Hunt: AI Agent Powered Game — Gradio Web App
"""

import os

import gradio as gr
from dotenv import load_dotenv
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse, Response

from game.config import (
    API_KEY_PATH,
    APP_DESC,
    APP_NAME,
    APP_URL,
    APP_VERSION,
    EXAMPLE_COMMANDS,
)
from game.content import NARRATOR_INTRO
from game.router import Router
from game.ui_shared import (
    GRADIO_CSS,
    TIP_TEXT,
    build_gradio_theme,
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


def handle_chat(message, history):
    # history is a list of {"role": "...", "content": "..."} dicts with type="messages"
    text = message["content"] if isinstance(message, dict) else str(message)
    if not _ROUTER.ready:
        return (
            "⚠️ Dependency missing or not importable: game.engine.respond_narrator. "
            "Ensure the agents framework is installed and imports succeed."
        )
    try:
        # Pass history through; Router currently ignores it but may use it later
        return _ROUTER.handle(text, history)
    except Exception as e:
        return f"⚠️ Error: {e!s}"


def build_app():
    if not has_api_key():
        raise EnvironmentError("OpenAI API key not found. Please check your .env file.")

    with gr.Blocks(
        title=APP_NAME,
        theme=build_gradio_theme(),
        css=GRADIO_CSS,
        analytics_enabled=False,
    ) as app:
        gr.Markdown(header_html(APP_NAME, APP_VERSION))
        gr.Markdown(card_html(APP_DESC, TIP_TEXT))

        ci = gr.ChatInterface(
            fn=handle_chat,
            type="messages",
            textbox=gr.Textbox(placeholder="Type your action...", autofocus=True),
            examples=EXAMPLE_COMMANDS,
            cache_examples=False,
            concurrency_limit=5,
        )

        def seed_intro():
            msgs = [{"role": "assistant", "content": NARRATOR_INTRO}]
            return msgs, msgs  # <- seed the visible chatbot AND the internal state

        # seed BOTH outputs: chatbot + state
        app.load(fn=seed_intro, outputs=[ci.chatbot, ci.chatbot_state])

        gr.Markdown(footer_html(APP_NAME))

    return app


demo = build_app()


# ----- FastAPI routes -----
@demo.app.get("/manifest.json")
def manifest():
    data = {
        "name": APP_NAME,
        "short_name": "Outlive",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#ffffff",
        "theme_color": "#4f46e5",
        "icons": [],
        "scope": "/",
        "id": APP_URL.rstrip("/") + "/",
    }
    return JSONResponse(data)


@demo.app.get("/robots.txt")
def robots():
    return PlainTextResponse(
        f"User-agent: *\nAllow: /\nSitemap: {APP_URL.rstrip('/')}/sitemap.xml\n"
    )


@demo.app.get("/sitemap.xml")
def sitemap():
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{APP_URL.rstrip("/")}/</loc></url>
</urlset>"""
    return Response(content=xml, media_type="application/xml")


if os.path.exists("favicon.ico"):

    @demo.app.get("/favicon.ico")
    def favicon():
        return FileResponse("favicon.ico", media_type="image/x-icon")


if __name__ == "__main__":
    demo.launch()
