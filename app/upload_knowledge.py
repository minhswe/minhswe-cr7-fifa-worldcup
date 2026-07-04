from app.ai.uploader import (
    ensure_file_search_store,
    upload_markdown_directory,
)


def main():
    store = ensure_file_search_store()

    upload_markdown_directory(store.name)


if __name__ == "__main__":
    main()