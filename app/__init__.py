"""
App package bootstrap for the Thriller Game demo.
Keeps shared constants in one place so Gradio/Streamlit shells can import them.
"""

import os

APP_NAME = "Thriller Game"
APP_DESC = "A near-future text thriller powered by a Narrator Agent."
APP_VERSION = "0.1.0"

# In case you want to serve absolute URLs for sitemap/manifest
APP_URL = os.getenv("APP_URL", "http://127.0.0.1:7860")

# Optional: where your .env lives (adjust as needed)
ENV_PATH = os.getenv("ENV_PATH", "../resources/openaiApiKey.env")

__all__ = [
    "APP_NAME",
    "APP_DESC",
    "APP_VERSION",
    "APP_URL",
    "ENV_PATH",
]
