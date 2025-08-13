# game/config.py
import os
from dotenv import load_dotenv

# Allow both repo-root and ../resources
load_dotenv(dotenv_path=os.getenv("ENV_PATH", "./resources/openaiApiKey.env"))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

APP_NAME = "Thriller Game"
MODEL = os.getenv("MODEL", "gpt-4o")
