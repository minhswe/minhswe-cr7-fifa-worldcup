from google import genai

from app.config import GEMINI_API_KEY


def get_client():
    return genai.Client(api_key=GEMINI_API_KEY)