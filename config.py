import os
from dotenv import load_dotenv

load_dotenv()

# X API Configuration
X_API_KEY = os.getenv("X_API_KEY")
X_API_SECRET = os.getenv("X_API_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")
X_BEARER_TOKEN = os.getenv("X_BEARER_TOKEN")

# LLM Configuration
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "claude")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Agent Configuration
POSTS_PER_RUN = int(os.getenv("POSTS_PER_RUN", 1000))
MAX_POSTS_PER_DAY = int(os.getenv("MAX_POSTS_PER_DAY", 10000))
REPORT_OUTPUT_DIR = os.getenv("REPORT_OUTPUT_DIR", "./reports")

# Ensure output directory exists
os.makedirs(REPORT_OUTPUT_DIR, exist_ok=True)
