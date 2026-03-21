"""Loads environment variables from .env and exposes application-level constants."""

import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY: str = os.environ.get("GROQ_API_KEY", "")
GROQ_API_BASE: str = os.environ.get("GROQ_API_BASE", "https://api.groq.com/openai/v1")
MODEL_NAME: str = os.environ.get("MODEL_NAME", "llama-3.1-8b-instant")

if not GROQ_API_KEY:
    raise EnvironmentError(
        "GROQ_API_KEY is not set. "
        "Create a .env file in the project root with: GROQ_API_KEY=your_key_here"
    )
