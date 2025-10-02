"""
Eternal Hunt: AI Agent Powered Game — Gradio Web App
"""

import os
from dotenv import load_dotenv
import datetime
import gradio as gr
from fastapi.responses import JSONResponse, PlainTextResponse, Response, FileResponse

from game.config import (
    APP_NAME,
    APP_DESC,
    APP_VERSION,
    APP_URL,
    EXAMPLE_COMMANDS,
    API_KEY_PATH,
)
from game.ui_shared import (
    TIP_TEXT,
    GRADIO_CSS,
    header_html,
    card_html,
    footer_html,
    has_api_key,
    build_gradio_theme,
)
from game.router import Router

# Load environment variables before importing game modules
if os.path.exists(".env"):
    load_dotenv()
elif os.path.exists(API_KEY_PATH):
    load_dotenv(dotenv_path=API_KEY_PATH)

# Single router instance per process
_ROUTER = Router()


def handle_chat(message, history):  # ChatInterface requires (message, history)
    if not _ROUTER.ready:
        return "⚠️ Router not ready. Check server logs."
    # history comes as list of [user, assistant] pairs in Gradio; normalize to tuples
    history = [
        (h[0], h[1]) if isinstance(h, list) else tuple(h) for h in (history or [])
    ]
    return _ROUTER.handle(message, history)


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

        gr.ChatInterface(
            fn=handle_chat,
            textbox=gr.Textbox(placeholder="Type your action...", autofocus=True),
            examples=EXAMPLE_COMMANDS,
            cache_examples=False,
            concurrency_limit=5,
        )

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
  <url><loc>{APP_URL.rstrip('/')}/</loc></url>
</urlset>"""
    return Response(content=xml, media_type="application/xml")


if os.path.exists("favicon.ico"):

    @demo.app.get("/favicon.ico")
    def favicon():
        return FileResponse("favicon.ico", media_type="image/x-icon")


if __name__ == "__main__":
    demo.launch()
