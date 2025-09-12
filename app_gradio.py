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
    API_KEY_PATH
)

# Load environment variables before importing game modules
if os.path.exists(".env"):
    load_dotenv()
elif os.path.exists(API_KEY_PATH):
    load_dotenv(dotenv_path=API_KEY_PATH)

# core deps
try:
    from game.api import respond_narrator
    DEPS_OK = True
except ModuleNotFoundError:
    DEPS_OK = False

# ----- ui helpers -----
def build_theme():
    return gr.themes.Soft(primary_hue="indigo", neutral_hue="slate").set(
        body_background_fill="*background_fill_primary",
    )

CSS = """
.gradio-container { max-width: 960px; margin: 0 auto }
.header { display: flex; gap: 12px; align-items: center; margin: 10px 0 6px }
.header .title { font-size: 1.5rem; font-weight: 800; letter-spacing: .2px; color: #111827 }
.header .meta { color: #4f46e5; font-size: .9rem; font-weight: 600 }
.section { border: 1px solid #e5e7eb; border-radius: 12px; padding: 14px 16px; background: #black }
.status { margin-bottom: 12px }
.footer { color: #6b7280; font-size: .85rem; text-align: center; margin-top: 14px }
"""

def handle_chat(message, history):  # <-- accept (message, history)
    if not DEPS_OK:
        return "⚠️ Could not load respond_narrator. Please check your dependencies."
    try:
        return respond_narrator(message)
    except Exception as e:
        return f"⚠️ Error: {e!s}"

def build_app():
    # Ensure API key is loaded before app starts
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise EnvironmentError("OpenAI API key not found. Please check your .env file.")

    with gr.Blocks(title=APP_NAME, theme=build_theme(), css=CSS, analytics_enabled=False) as app:
        # Header with improved contrast
        with gr.Row(elem_classes="header"):
            gr.Markdown(f"# {APP_NAME}", elem_classes="title")
            gr.Markdown(f"<span class='meta'>v{APP_VERSION}</span>", elem_id="app-version")
        
        # Status section with app description
        with gr.Row(elem_classes="status"):
            gr.Markdown(
                f"""<div class='section'>
                <p>{APP_DESC}</p>
                </div>"""
            )

        # Main chat interface
        gr.ChatInterface(
            fn=handle_chat,
            textbox=gr.Textbox(
                placeholder="Type your action...", 
                autofocus=True
            ),
            examples=EXAMPLE_COMMANDS,
            cache_examples=False,
            concurrency_limit=5
        )

        # Footer
        gr.Markdown(
            f"<div class='footer'>© {datetime.datetime.now().year} — {APP_NAME}</div>"
        )
    
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