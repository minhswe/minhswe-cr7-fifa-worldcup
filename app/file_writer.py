from pathlib import Path

from slugify import slugify


OUTPUT_DIR = Path("data/markdown")


def save_markdown(article: dict, markdown: str) -> Path:
    """
    Save a markdown article as <slug>.md
    """

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    slug = slugify(article["title"])
    filename = f"{slug}.md"

    # Save each file as <slug>.md
    file_path = OUTPUT_DIR / filename

    # Avoid overwriting if two articles have the same title
    if file_path.exists():
        filename = f"{slug}-{article['id']}.md"
        file_path = OUTPUT_DIR / filename

    file_path.write_text(markdown, encoding="utf-8")

    return file_path