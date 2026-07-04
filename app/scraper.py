import os
from dotenv import load_dotenv
import requests

load_dotenv()
BASE_URL = os.getenv("BASE_URL")


def fetch_articles():
    articles = []
    current_url = BASE_URL
    while current_url:
        print(f"loading from: {current_url}")
        response = requests.get(current_url)
        response.raise_for_status()
        data = response.json()
        page = data["page"]
        page_count = data["page_count"]

        print(f"Fetched page {page}/{page_count}")
        current_page_articles = data.get("articles", [])
        articles.extend(current_page_articles)
        current_url = data.get("next_page")

    return articles
