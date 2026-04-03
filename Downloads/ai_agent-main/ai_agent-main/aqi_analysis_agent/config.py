"""
Configuration settings for the AQI Analysis Agent.
Author: Hazbilal3
"""
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys
# These are optional defaults; the UI allows overriding them
FIRECRAWL_API_KEY = os.getenv("FIRECRAWL_API_KEY", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# App Constants
APP_TITLE = "AQI Analysis Agent"
APP_ICON = "🌍"

# Logging setup
def setup_logging(level=logging.INFO):
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )
