"""
Shared UI helpers for Eternal Hunt frontends (Gradio + Streamlit).

Centralizes:
- Typography/width CSS
- Header HTML (title + version)
- Description "card" HTML with shared tip
- Footer HTML
- API key presence check
- Gradio theme (lazy import to avoid hard dep in Streamlit-only environments)
"""

from __future__ import annotations
import os
import datetime

# --- Shared copy/text ---------------------------------------------------------

TIP_TEXT = "Try “Look around”, “Inventory”, “Open the door”."

# --- Shared HTML snippets -----------------------------------------------------


def header_html(app_name: str, app_version: str) -> str:
    """Header row with title + muted version text (matches both UIs)."""
    return f"""
    <div class="app-header">
      <div class="app-title">{app_name}</div>
      <div class="app-meta">v{app_version}</div>
    </div>
    """


def card_html(app_desc: str, tip_text: str = TIP_TEXT) -> str:
    """Framed description card with helper tip beneath."""
    return f"""
    <div class="card">
      <p>{app_desc}</p>
      <div class="tip">{tip_text}</div>
    </div>
    """


def footer_html(app_name: str) -> str:
    year = datetime.datetime.now().year
    return f"<div class='footer'>© {year} — {app_name}</div>"


# --- CSS tokens ---------------------------------------------------------------

# Gradio uses different root containers than Streamlit, so keep two CSS strings.
GRADIO_CSS = """
/* Centered narrow layout, consistent with Streamlit */
.gradio-container { max-width: 900px; margin: 0 auto; }

/* Header */
.app-header { display:flex; align-items:center; gap:12px; margin:10px 0 6px; }
.app-title  { font-weight:800; font-size:1.6rem; letter-spacing:0.2px; color:#111827; }
.app-meta   { color:#6b7280; font-size:0.95rem; }

/* Card for description + tip */
.card { border:1px solid #e5e7eb; border-radius:12px; padding:14px 16px; background:#ffffff; }
.tip  { color:#6b7280; font-size:0.9rem; margin-top:6px; }

/* Footer */
.footer { color:#6b7280; font-size:0.85rem; text-align:center; margin-top:14px; }
"""

STREAMLIT_CSS = """
/* Centered narrow layout */
.main .block-container { max-width: 900px; }

/* Header */
.app-header { display:flex; align-items:center; gap:12px; margin-top:8px; }
.app-title  { font-weight:800; font-size:1.6rem; letter-spacing:0.2px; color:#111827; }
.app-meta   { color:#6b7280; font-size:0.95rem; }

/* Card for description + tip (mirrors Gradio) */
.card { border:1px solid #e5e7eb; border-radius:12px; padding:14px 16px; background:#ffffff; }
.tip  { color:#6b7280; font-size:0.9rem; margin-top:6px; }

/* Footer */
.footer { color:#6b7280; font-size:0.85rem; text-align:center; margin-top:12px; }
"""

# --- Utilities ----------------------------------------------------------------


def has_api_key(var_name: str = "OPENAI_API_KEY") -> bool:
    """Return True if an API key-like env var is set and non-empty."""
    return bool(os.getenv(var_name))


def build_gradio_theme():
    """
    Lazy-import Gradio and return a Soft theme aligned to our neutral palette.
    Keeping import inside avoids requiring gradio when only running Streamlit.
    """
    import gradio as gr  # lazy

    return gr.themes.Soft(primary_hue="indigo", neutral_hue="slate").set(
        body_background_fill="*background_fill_primary",
    )
