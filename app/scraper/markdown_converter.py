from markdownify import markdownify as md
from bs4 import BeautifulSoup


def article_to_markdown(article: dict) -> str:
    """
    Convert a Zendesk article to clean Markdown.
    """

    title = article.get("title", "").strip()
    html = article.get("body", "")
    if not html:
        return f"# {title}"

    soup = BeautifulSoup(html, "html.parser")

    # Remove nav/ads.
    for tag in soup.select("nav, footer, aside"):
        tag.decompose()

    # Convert cleaned HTML -> Markdown
    markdown_body = md(
        str(soup),
        heading_style="ATX",
        bullets="-",
        strip=["style", "script"],
    ).strip()

    markdown = f"""# {title}
    
{markdown_body}

---

Article URL: {article.get("html_url")}
"""
    return markdown
