import hashlib

from app.ai.uploader import (
    ensure_file_search_store,
    replace_document,
    upload_markdown_file,
    find_document,
)
from app.scraper.exporter import export_article
from app.scraper.scraper import fetch_articles
from app.sync.state import (
    load_state,
    save_state,
    get_article_state,
    update_article_state,
)


def calculate_hash(article: dict) -> str:
    """
    Calculate SHA-256 hash of an article's content.
    """
    content = article.get("body", "")

    return hashlib.sha256(
        content.encode("utf-8")
    ).hexdigest()


def run_sync():
    """
    Synchronize Zendesk articles with Gemini File Search Store.
    """

    print("Starting synchronization...")

    state = load_state()
    store = ensure_file_search_store()

    articles = fetch_articles()

    added = 0
    updated = 0
    skipped = 0

    for article in articles:

        article_id = str(article["id"])
        updated_at = article["updated_at"]
        content_hash = calculate_hash(article)

        saved_state = get_article_state(state, article_id)

        markdown_file = export_article(article)

        # -----------------------------
        # New article
        # -----------------------------
        if saved_state is None:

            document = find_document(
                store.name,
                markdown_file.stem,
            )

            if document is None:
                upload_markdown_file(
                    store.name,
                    markdown_file,
                )
                print(f"[ADDED] {article['title']}")
                added += 1
            else:
                print(f"[SKIPPED] {article['title']}")
                skipped += 1

                update_article_state(
                    state,
                    article_id,
                    updated_at,
                    content_hash,
                )

        # -----------------------------
        # Updated article
        # -----------------------------
        elif (
                saved_state["updated_at"] != updated_at
                or saved_state["hash"] != content_hash
        ):

            replace_document(
                store.name,
                markdown_file,
            )

            update_article_state(
                state,
                article_id,
                updated_at,
                content_hash,
            )

            updated += 1

            print(f"[UPDATED] {article['title']}")

        # -----------------------------
        # Unchanged
        # -----------------------------
        else:

            skipped += 1

    save_state(state)

    print("\n========== Sync Summary ==========")
    print(f"Fetched : {len(articles)}")
    print(f"Added   : {added}")
    print(f"Updated : {updated}")
    print(f"Skipped : {skipped}")
    print("==================================")
