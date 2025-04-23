import os
from dotenv import load_dotenv

load_dotenv()

dynamic_config = {
    'GAME_LANGUAGE': 'English',
    'LOCALE': any
}

# LLM
HF_API_KEY = os.getenv("HF_API_KEY")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
MISTRAL_MODEL_NAME = "mistral-small-latest"
HF_MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.3"
HF_MODEL_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.3"

#Telegram client
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


# Game Settings
STORY_STRUCT_MOCK = True