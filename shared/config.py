import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
GOOGLE_CREDENTIALS = os.getenv("GOOGLE_CREDENTIALS")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
HF_KEY = os.getenv("HUGGINGFACE_API_KEY")
ALLOWED_DISCORD_CHANNEL_ID = os.getenv("ALLOWED_DISCORD_CHANNEL_ID")

BASE_URL = "http://localhost:8000/"
