"""
Gradio shell for the Thriller Game.
- Small, readable Blocks layout
- Theme + CSS polish
- Meta routes: /manifest.json, /robots.txt, /sitemap.xml (via FastAPI)
"""

import datetime
import os

import gradio as gr
import nest_asyncio
from dotenv import load_dotenv
from fastapi.responses import JSONResponse, PlainTextResponse, Response, FileResponse
from game.engine import autoload_state


from app import APP_NAME, APP_DESC, APP_VERSION, APP_URL, ENV_PATH
from app.router import Router

# ---- env + asyncio ----
load_dotenv(dotenv_path=ENV_PATH)
nest_asyncio.apply()

router = Router()

# ---- Try to load saved state at startup ----
# This will automatically load the last saved game state if available.
autoload_state()

# ---- UI helpers ----
def build_theme():
    return gr.themes.Soft(primary_hue="indigo", neutral_hue="slate").set(
        body_background_fill="*background_fill_primary",
    )


CSS = """
.gradio-container{max-width:960px;margin:0 auto}
.header{display:flex;gap:12px;align-items:center;margin:10px 0 6px}
.header .title{font-size:1.5rem;font-weight:800;letter-spacing:.2px}
.header .meta{color:#6b7280;font-size:.9rem}
.section{border:1px solid #e5e7eb;border-radius:12px;padding:14px 16px;background:#fff;box-shadow:0 1px 2px rgba(0,0,0,.03)}
.footer{color:#6b7280;font-size:.85rem;text-align:center;margin-top:14px}
"""


def handle_chat(message, history):
    return router.handle(message, history)


def build_app():
    with gr.Blocks(title=APP_NAME, theme=build_theme(), css=CSS, analytics_enabled=False) as app:
        # Header
        with gr.Row(elem_classes="header"):
            gr.Markdown(f"**{APP_NAME}**", elem_classes="title")
            gr.Markdown(f"<span class='meta'>v{APP_VERSION}</span>", elem_id="app-version")

        # Intro / How-to
        with gr.Row():
            gr.Markdown(
                f"<div class='section'><p>{APP_DESC}</p>"
                "<p><strong>How to play:</strong> try “Look around”, “Inventory”, “Open the door”.</p></div>"
            )

        # Chat
        gr.ChatInterface(
            fn=handle_chat,
            textbox=gr.Textbox(placeholder="e.g., Look around the room", autofocus=True),
            examples=["Look around", "Inventory", "Open the door", "Run outside"],
            cache_examples=False,
            concurrency_limit=5,
        )

        # Footer
        gr.Markdown(f"<div class='footer'>© {datetime.datetime.now().year} — {APP_NAME}</div>")

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
    return PlainTextResponse(f"User-agent: *\nAllow: /\nSitemap: {APP_URL.rstrip('/')}/sitemap.xml\n")


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
    # Use `python -m app.main` or `python app/main.py`
    demo.launch()
