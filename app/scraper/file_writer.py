from pathlib import Path

from slugify import slugify

OUTPUT_DIR = Path("data/markdown")


def save_markdown(article: dict, markdown: str) -> Path:
    """
    Save a markdown article as <slug>.md.
    Overwrite existing file if it already exists.
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    slug = slugify(article["title"])
    file_path = OUTPUT_DIR / f"{slug}.md"

    file_path.write_text(markdown, encoding="utf-8")

    return file_path