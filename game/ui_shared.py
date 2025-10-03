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

import gradio as gr

# --- Shared copy/text ---------------------------------------------------------

TIP_TEXT = "“Look around”, “Inventory”, “Open the door”."

# --- Shared HTML snippets -----------------------------------------------------


def header_html(app_name: str, version: str) -> str:
    return f"""
    <div class="app-header">
      <div class="app-title">{app_name}</div>
      <div class="app-meta">v{version}</div>
    </div>
    """


def card_html(desc: str, tip: str) -> str:
    return f"""
    <div class="card">
      <p>{desc}</p>
      <p style="margin-top:.5rem;"><strong>Try</strong> {tip}</p>
    </div>
    """


def footer_html(app_name: str) -> str:
    return f"<div class='footer'>© {__import__('datetime').datetime.now().year} — {app_name}</div>"


# --- CSS tokens ---------------------------------------------------------------

# Gradio uses different root containers than Streamlit, so keep two CSS strings.
GRADIO_CSS = """
/* --- Layout & header (shared) --- */
.gradio-container { max-width: 960px; margin: 0 auto; }
.app-header { display:flex; gap:12px; align-items:flex-end; margin:10px 0 6px; }
.app-title  { font-weight:800; letter-spacing:.2px; }
.app-meta   { font-size:.9rem; }

/* Card block used for the description/tip */
.card { border:1px solid #e5e7eb; border-radius:12px; padding:14px 16px; background:#ffffff; box-shadow:0 1px 2px rgba(0,0,0,.04); }
.card, .card p, .card strong, .card em { color:#111827; }   /* ensure full contrast in light mode */

/* Light-mode title color (beat .prose defaults) */
.gradio-container .prose .app-title,
.gradio-container .app-title {
  color: #2B2B2B !important;  /* your desired light color */
}

.footer { color:#6b7280; font-size:.85rem; text-align:center; margin-top:14px; }

/* Chat bubbles – light mode defaults */
.gradio-container .message.user,
.gradio-container .message.user .markdown,
.gradio-container .message.user .markdown * {
  color: #1f2937 !important;   /* slate-800 */
}

.gradio-container .message.bot,
.gradio-container .message.bot .markdown,
.gradio-container .message.bot .markdown * {
  color: #111827 !important;   /* gray-900 */
}

/* Make markdown/prose in messages fully opaque & inheriting color */
.gradio-container .message .markdown,
.gradio-container .message .markdown * {
  color: inherit !important;
  opacity: 1 !important;
}

/* Inputs (light) */
.gradio-container input[type="text"], .gradio-container textarea {
  background:#ffffff !important; color:#111827 !important; border-color:#d1d5db !important;
}

/* --- Dark mode overrides --- */
@media (prefers-color-scheme: dark) {
  :root, .gradio-container { background:#0b0f19; }

  .app-title { color:#9bacde !important; font-size:2rem; line-height:1.2; }
  .app-meta  { color:#9ca3af; }

  .card { background:#0f172a; border-color:#1f2937; }
  .card, .card p, .card strong, .card em { color:#e5e7eb; }

  .footer { color:#9ca3af; }

  /* Chat bubbles (dark, higher contrast) */
  .gradio-container .message.user {
    background:#121826 !important; color:#e5e7eb !important; border-color:#1f2937 !important;
  }
  .gradio-container .message.bot  {
    background:#0c1322 !important; color:#e5e7eb !important; border-color:#1f2937 !important;
  }

  /* Ensure markdown stays bright in dark bubbles */
  .gradio-container .message .markdown,
  .gradio-container .message .markdown * {
    color: inherit !important;
    opacity: 1 !important;
  }

  /* Inputs (dark) */
  .gradio-container input[type="text"], .gradio-container textarea {
    background:#0f172a !important; color:#e5e7eb !important; border-color:#334155 !important;
  }
  .gradio-container ::placeholder { color:#a3b0c2 !important; }
}
"""


STREAMLIT_CSS = """
/* Centered narrow layout */
.main .block-container { max-width: 900px; }

/* Header + meta */
.app-header { display:flex; align-items:center; gap:12px; margin-top:8px; }
.app-title { font-weight:800; font-size:1.6rem; letter-spacing:0.2px; color:#111827; }
.app-meta { color:#6b7280; font-size:0.95rem; }

/* Card for description + tip (mirrors Gradio) */
.card { border:1px solid #e5e7eb; border-radius:12px; padding:14px 16px; background:#ffffff; }
.tip { color:#6b7280; font-size:0.9rem; margin-top:6px; }

/* Footer */
.footer { color:#6b7280; font-size:0.85rem; text-align:center; margin-top:12px; }

/* Chat (light) */
[data-testid="stChatMessage"] { border:1px solid #e5e7eb; background:#ffffff; border-radius:12px; }
[data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] { color:#111827; }

/* ---------- Dark mode ---------- */
@media (prefers-color-scheme: dark) {
  .stApp { background:#0b0f19; }
  .app-title { color:#e5e7eb; }
  .app-meta { color:#9ca3af; }
  .card { background:#0f172a; border-color:#1f2937; }
  .tip, .footer { color:#9ca3af; }

  /* Chat bubbles */
  [data-testid="stChatMessage"] { background:#0f172a; border-color:#1f2937; }
  [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] { color:#e5e7eb; }
  /* Make the user message container a tad darker */
  [data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) { background:#0b1220; }

  /* Inputs */
  .stTextInput input, .stTextArea textarea {
    background:#0f172a !important; color:#e5e7eb !important; border-color:#334155 !important;
  }
  .stTextInput input::placeholder, .stTextArea textarea::placeholder { color:#94a3b8 !important; }
}
"""


# --- Utilities ----------------------------------------------------------------


def has_api_key(var_name: str = "OPENAI_API_KEY") -> bool:
    """Return True if an API key-like env var is set and non-empty."""
    return bool(os.getenv(var_name))


PRIMARY = "indigo"  # your accent
NEUTRAL = "slate"  # base gray scale


def build_gradio_theme():
    """
    Base theme with stronger contrast; CSS below handles precise dark tweaks.
    """
    return gr.themes.Soft(primary_hue=PRIMARY, neutral_hue=NEUTRAL).set(
        # General text + links
        body_text_color="#111827",  # darkened in CSS for dark mode
        link_text_color="#4f46e5",
        # Panels / blocks
        block_background_fill="#ffffff",  # darkened in CSS for dark mode
        block_border_color="#e5e7eb",
        block_title_text_color="#111827",
        # Inputs / chat
        input_background_fill="#ffffff",
        input_border_color="#d1d5db",
        # Subtle elevations
        shadow_drop="0 1px 2px rgba(0,0,0,.06)",
        shadow_spread="0 0 0 rgba(0,0,0,0)",
    )
