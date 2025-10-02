"""
Main for Eternal Hunt.
- Shared theme/CSS + header/card/footer via game.ui_shared
- Single Router entrypoint
- Meta routes: /manifest.json, /robots.txt, /sitemap.xml (via FastAPI)
"""

import os
import gradio as gr
from dotenv import load_dotenv
from fastapi.responses import JSONResponse, PlainTextResponse, Response, FileResponse

from game.engine import autoload_state
from game.router import Router
from game.config import (
    APP_NAME,
    APP_DESC,
    APP_VERSION,
    APP_URL,
    API_KEY_PATH,
    EXAMPLE_COMMANDS,
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

# ---- env ----
# Load .env or fallback API key path from config
if os.path.exists(".env"):
    load_dotenv()
elif API_KEY_PATH and os.path.exists(API_KEY_PATH):
    load_dotenv(dotenv_path=API_KEY_PATH)

# ---- Try to load saved state at startup ----
autoload_state()

# ---- Router (single instance) ----
_ROUTER = Router()


# ---- UI handlers ----
def handle_chat(message, history):
    """Gradio ChatInterface callback (message, history)."""
    if not _ROUTER.ready:
        return "⚠️ Router not ready. Check server logs."
    # history can be list[list[str,str]]; normalize to list[tuple[str,str]]
    history = [
        (h[0], h[1]) if isinstance(h, list) else tuple(h) for h in (history or [])
    ]
    return _ROUTER.handle((message or "").strip(), history)


def build_app():
    # Fail fast if no key; mirrors our other Gradio entry
    if not has_api_key():
        raise EnvironmentError(
            "OpenAI API key not found. Please check your .env or API_KEY_PATH."
        )

    with gr.Blocks(
        title=APP_NAME,
        theme=build_gradio_theme(),
        css=GRADIO_CSS,
        analytics_enabled=False,
    ) as app:
        # Header
        gr.Markdown(header_html(APP_NAME, APP_VERSION))

        # Intro / How-to (shared card + tip)
        gr.Markdown(card_html(APP_DESC, TIP_TEXT))

        # Chat (shared examples)
        gr.ChatInterface(
            fn=handle_chat,
            textbox=gr.Textbox(placeholder="Type your action...", autofocus=True),
            examples=EXAMPLE_COMMANDS,
            cache_examples=False,
            concurrency_limit=5,
        )

        # Footer
        gr.Markdown(footer_html(APP_NAME))

    return app


demo = build_app()


# ---- Meta routes (FastAPI mounted by Gradio) ----
@demo.app.get("/manifest.json")
def manifest():
    data = {
        "name": APP_NAME,
        "short_name": "Thriller",
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


# Optional favicon passthrough if you drop a local file next to your entrypoint
if os.path.exists("favicon.ico"):

    @demo.app.get("/favicon.ico")
    def favicon():
        return FileResponse("favicon.ico", media_type="image/x-icon")


if __name__ == "__main__":
    # Use: python main.py
    demo.launch()
