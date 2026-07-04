# app/test_store.py

from app.ai.client import get_client

client = get_client()

for store in client.file_search_stores.list():
    print(store)