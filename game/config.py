"""
Shared configuration for the game UIs
"""

import os

# App configuration
APP_NAME = "Eternal Hunt: AI Agent Powered Game"
APP_DESC = "You possess a rare gene for extreme longevity. Someone powerful wants it. Run, hide, survive. Powered by OpenAI Agents."
APP_VERSION = "0.1.0"
APP_URL = os.getenv("APP_URL", "http://127.0.0.1:7860")
API_KEY_PATH = "./resources/openaiApiKey.env"

# Example commands
EXAMPLE_COMMANDS = ["Look around", "Check phone", "Open the door", "Run outside"]

# Default model configuration
MODEL = "gpt-4"
