from app.scraper.exporter import export_articles

def main():
    total = export_articles()
    print(f"Saved {total} markdown files.")


if __name__ == "__main__":
    main()