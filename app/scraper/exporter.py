from app.scraper.scraper import fetch_articles
from app.scraper.markdown_converter import article_to_markdown
from app.scraper.file_writer import save_markdown


def export_articles() -> int:
    """Fetch articles, convert them to Markdown, and save them."""

    print("Fetching articles...")
    articles = fetch_articles()
    print(f"Fetched {len(articles)} articles.")

    print("Converting articles to Markdown...")

    for article in articles:
        markdown = article_to_markdown(article)
        save_markdown(article, markdown)

    return len(articles)