"""
Thriller Game — Gradio Web App
A cleaner, production-leaning structure (functions, constants, minimal comments).
"""
import os
import datetime
import nest_asyncio
import gradio as gr
from dotenv import load_dotenv
from fastapi.responses import JSONResponse, PlainTextResponse, Response, FileResponse

# ----- configuration -----
APP_NAME = "Thriller Game"
APP_DESC = "A near-future text thriller powered by a Narrator Agent."
APP_VERSION = "0.1.0"
APP_URL = os.getenv("APP_URL", "http://127.0.0.1:7860")
ENV_PATH = "../resources/openaiApiKey.env"

# env + asyncio
load_dotenv(dotenv_path=ENV_PATH)
nest_asyncio.apply()

# core deps
try:
    from game.thriller_module import respond_narrator
except ModuleNotFoundError:
    def respond_narrator(_msg: str) -> str:
        return "Dependency missing: 'openai-agents' (module 'agents'). Please run: pip install openai-agents"

# ----- ui pieces -----
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
    try:
        return respond_narrator(message)
    except Exception as e:
        return f"⚠️ Error: {e!s}"

def build_app():
    with gr.Blocks(title=APP_NAME, theme=build_theme(), css=CSS, analytics_enabled=False) as app:
        with gr.Row(elem_classes="header"):
            gr.Markdown(f"**{APP_NAME}**", elem_classes="title")
            gr.Markdown(f"<span class='meta'>v{APP_VERSION}</span>", elem_id="app-version")
        with gr.Row():
            gr.Markdown(f"<div class='section'><p>{APP_DESC}</p><p><strong>How to play:</strong> try “Look around”, “Inventory”, “Open the door”.</p></div>")
        gr.ChatInterface(
            fn=handle_chat,
            type="messages",
            textbox=gr.Textbox(placeholder="e.g., Look around the room", autofocus=True),
            examples=["Look around", "Inventory", "Open the door", "Run outside"],
            cache_examples=False,
            concurrency_limit=5,
        )
        gr.Markdown(f"<div class='footer'>© {datetime.datetime.now().year} — {APP_NAME}</div>")
    return app

demo = build_app()

# ----- meta routes -----
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

if os.path.exists("favicon.ico"):
    @demo.app.get("/favicon.ico")
    def favicon():
        return FileResponse("favicon.ico", media_type="image/x-icon")

if __name__ == "__main__":
    demo.launch()
