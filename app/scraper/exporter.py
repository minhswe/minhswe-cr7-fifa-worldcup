from app.scraper.scraper import fetch_articles
from app.scraper.markdown_converter import article_to_markdown
from app.scraper.file_writer import save_markdown


def export_article(article: dict):
    """
    Convert a single article to Markdown and save it.

    Returns:
        Path: Path to the saved markdown file.
    """

    markdown = article_to_markdown(article)

    return save_markdown(article, markdown)


def export_articles() -> int:
    """
    Fetch all articles, convert them to Markdown, and save them.
    """

    print("Fetching articles...")
    articles = fetch_articles()
    print(f"Fetched {len(articles)} articles.")

    print("Converting articles to Markdown...")

    for article in articles:
        export_article(article)

    return len(articles)