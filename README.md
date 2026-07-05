##Local Setup

### 1. Clone repo

git clone https://github.com/minhswe/minhswe-cr7-fifa-worldcup

cd minhswe-cr7-fifa-worldcup

### 2. Install dependencies

```shell
pip install -r requirements.txt
```

### 3. Configure environment

Create a `.env` file based on `.env.example`:

- `GEMINI_API_KEY`: API key for Gemini model access
- `BASE_URL`: Source website for scraping articles
- `FILE_SEARCH_STORE_NAME`: Vector store / knowledge base ID
- `GEMINI_MODEL`: Model name (e.g. gemini-1.5-flash)
- `MAX_ARTICLES`: Maximum number of articles to scrape
- `MAX_UPLOAD_FILES`: Limit for uploaded files per sync run

### 4. Run scraper + sync

```shell
python -m app.main
```

## Docker

### 1. Build image

```bash
docker build -t knowledge-sync .
```

### 2. Run

```shell
docker run --rm --env-file .env knowledge-sync
```

Notes:

- --rm: removes container after execution
- --env-file: loads environment variables from .env
- Container runs once and exits with status 0 if successful

## Screenshot

Question:
> "How do I add a YouTube video?"

Output:

- Step-by-step answer
- With cited article URLs

![Assistant Demo](./assets/output-with-right-answer.png)

## Daily Sync Job

The system runs automatically every day via GitHub Actions:

🔗 GitHub Actions Logs:
https://github.com/minhswe/minhswe-cr7-fifa-worldcup/actions

> **Note:**
> During testing, the workflow schedule was temporarily configured to run every 5 minutes. However, GitHub Actions
> scheduled workflows are best-effort rather than guaranteed to execute at the exact scheduled time. In practice, the
> workflow may be delayed, sometimes by several hours, depending on GitHub's scheduling and runner availability. This
> behavior is a limitation of GitHub Actions scheduling rather than the synchronization logic itself.

## Vector Store Sync Strategy

This project uses an explicit delete-and-reupload strategy when synchronizing updated documents.

Instead of relying on provider-specific overwrite behavior, the sync process:

- Detects changes using updated_at and a SHA-256 content hash.
- Deletes the existing document (if present).
- Uploads the latest Markdown version.

This approach keeps the knowledge base free of duplicate or stale documents and makes the synchronization logic
consistent across different vector store providers.