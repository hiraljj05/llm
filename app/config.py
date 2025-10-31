from pathlib import Path
import os

# Base folder for generated projects
OUTPUT_BASE = Path(os.getenv("OUTPUT_BASE", "./generated_projects")).resolve()
OUTPUT_BASE.mkdir(parents=True, exist_ok=True)

# LLM settings
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# retry settings
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "3"))
