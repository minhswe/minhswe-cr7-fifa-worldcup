import time
import os
from pathlib import Path
from dotenv import load_dotenv

from app.ai.client import get_client

load_dotenv()
client = get_client()
MARKDOWN_DIR = Path("data/markdown")
STORE_NAME = os.getenv("FILE_SEARCH_STORE_NAME", "optisigns-knowledge-base")


def get_store_by_name(display_name: str):
    for store in client.file_search_stores.list():
        if store.display_name == display_name:
            return store

    return None


def ensure_file_search_store():
    store = get_store_by_name(STORE_NAME)

    if store:
        print(f"Using existing store: {store.name}")
        return store

    store = client.file_search_stores.create(
        config={
            "display_name": STORE_NAME,
            "embedding_model": "models/gemini-embedding-2",
        }
    )

    print(f"Created store: {store.name}")

    return store


def upload_markdown_file(store_name: str, file_path: Path):
    """
    Upload a single markdown file to the File Search Store.
    """

    operation = client.file_search_stores.upload_to_file_search_store(
        file=file_path,
        file_search_store_name=store_name,
        config={
            "display_name": file_path.stem,
        },
    )

    while not operation.done:
        time.sleep(2)
        operation = client.operations.get(operation)

    print(f"Uploaded: {file_path.name}")


def upload_markdown_directory(store_name: str):
    """
    Upload all markdown files inside data/markdown.
    """

    markdown_files = sorted(MARKDOWN_DIR.glob("*.md"))

    if not markdown_files:
        raise FileNotFoundError(
            f"No markdown files found in {MARKDOWN_DIR}"
        )

    print(f"Found {len(markdown_files)} markdown files.")

    total = len(markdown_files)

    for index, markdown_file in enumerate(markdown_files, start=1):
        print(f"[{index}/{total}] Uploading {markdown_file.name}")

        upload_markdown_file(
            store_name,
            markdown_file,
        )
    print("\n========== Embedding Summary ==========")
    print(f"Files embedded : {len(markdown_files)}")
    print(f"Store          : {store_name}")
    print("Chunking       : Automatic (Gemini File Search)")
    print("=======================================")
