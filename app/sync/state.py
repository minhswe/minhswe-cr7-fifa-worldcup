import json
from pathlib import Path

STATE_FILE = Path("data/state.json")


def load_state() -> dict:
    """
    Load synchronization state from disk.

    Returns:
        dict: {
            article_id: {
                "updated_at": "...",
                "hash": "..."
            }
        }
    """

    if not STATE_FILE.exists():
        return {}

    with STATE_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)


def save_state(state: dict) -> None:
    """
    Save synchronization state to disk.
    """

    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)

    with STATE_FILE.open("w", encoding="utf-8") as file:
        json.dump(state, file, indent=4, ensure_ascii=False)


def get_article_state(state: dict, article_id: str) -> dict | None:
    """
    Get the saved state of an article.
    """

    return state.get(article_id)


def update_article_state(
        state: dict,
        article_id: str,
        updated_at: str,
        content_hash: str,
) -> None:
    """
    Update an article's synchronization state.
    """

    state[article_id] = {
        "updated_at": updated_at,
        "hash": content_hash,
    }