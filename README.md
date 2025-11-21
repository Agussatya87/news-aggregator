# AI News Aggregator

AI-powered system that ingests trusted RSS feeds, scrapes full articles, summarizes them with an on-prem LLM (Ollama), classifies topic & sentiment, and serves the curated feed through a FastAPI backend and Streamlit dashboard.

---

![Email-style AI digest](./Email_news.png)

---

![RSS ingestion log](./getData_RSS.png)

---

![Streamlit dark UI](./Web_UI_NEWS.png)

## Table of Contents
1. [Architecture](#architecture)
2. [Features](#features)
3. [Technology Stack](#technology-stack)
4. [Prerequisites](#prerequisites)
5. [Quick Start](#quick-start)
6. [Backend API](#backend-api)
7. [RSS Ingestion Worker](#rss-ingestion-worker)
8. [Streamlit Frontend](#streamlit-frontend)
9. [Environment Variables](#environment-variables)
10. [Development Tips](#development-tips)
11. [Roadmap Ideas](#roadmap-ideas)

## Architecture
- **Ingestion Worker (`backend/ingestion_rss.py`)**  
  Fetches RSS feeds (BBC News by default), scrapes full HTML for richer content & hero images, and calls the LLM summarizer.
- **LLM Summarizer (`backend/config.py`)**  
  Wraps an Ollama model (`llama3.1` by default) to produce a factual summary, topic, and sentiment JSON payload.
- **Persistence Layer**  
  SQLAlchemy models (`backend/models.py`) store normalized news entries (title, content, summary, topic, sentiment, published date, image, timestamps) in PostgreSQL.
- **REST API (`backend/main.py`)**  
  FastAPI exposes CRUD endpoints for Streamlit or third-party clients: create/import news, list with filters (`topic`, `q`, pagination), fetch by id.
- **Streamlit UI (`frontend/streamlit_app.py`)**  
  Presents a newsroom dashboard with filters, image preview, AI summary, sentiment badge, and link to the original source.

## Features
- Automatic scraping + deduplication of RSS items.
- LLM-enhanced summarization (3–6 sentences), topic classification, sentiment analysis.
- Topic & keyword filtering via API or Streamlit sidebar.
- Image enrichment using RSS and HTML fallbacks (OG tags, `<figure>`, first `<img>`).
- Resilient fallbacks if LLM call fails—news still persists with default metadata.
- Configurable feed list; simply append new entries in `RSS_SOURCES`.
- Docker-friendly layout; env variables handled via `.env`.

## Technology Stack
| Layer | Tools |
|-------|-------|
| LLM | [Ollama](https://ollama.com) + `llama3.1` |
| API | FastAPI, Pydantic, SQLAlchemy |
| DB  | PostgreSQL |
| Worker | feedparser, requests, BeautifulSoup |
| UI | Streamlit |
| Tooling | python-dotenv, uvicorn |

## Prerequisites
- Python 3.10+
- PostgreSQL instance (local Docker or managed service)
- [Ollama](https://ollama.com) installed with `ollama pull llama3.1`
- Node-free environment (Streamlit is Python-based)

## Quick Start
```bash
# 1. Clone & prepare environments
git clone <repo> news-aggregator && cd news-aggregator
python -m venv venv && source venv/bin/activate  # Use .\venv\Scripts\activate on Windows

# 2. Backend deps
pip install -r backend/requirements.txt

# 3. Frontend deps (optional separate venv)
pip install -r frontend/requirements.txt

# 4. Configure .env (see section below)
cp .env.example .env && edit .env

# 5. Ensure PostgreSQL is running and accessible
createdb news_aggregator  # or via UI/Docker

# 6. Start backend API
uvicorn backend.main:app --host 0.0.0.0 --port 8000

# 7. Run ingestion at least once
python -m backend.ingestion_rss

# 8. Launch Streamlit dashboard
streamlit run frontend/streamlit_app.py
```

## Backend API
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/news` | `POST` | Create/import a news item (used internally by ingestion, but available for manual inserts). |
| `/news` | `GET`  | List news with optional `topic`, `q`, `limit` (1–100), `offset`. Sorted by `published_at` then `created_at`. |
| `/news/{news_id}` | `GET` | Retrieve a single news item. |

All responses use `backend/schemas.py` (`NewsOut`, `NewsListResponse`). Errors (404, validation) are handled by FastAPI.

## RSS Ingestion Worker
1. Define feeds in `RSS_SOURCES` (name + RSS URL).  
2. Worker fetches entries, deduplicates by URL, and attempts to scrape the article page for full text + image.  
3. Calls `summarize_and_tag` to enrich metadata.  
4. Persists to DB and logs status, e.g.:
   ```
   [INFO] BBC News entries: 25
   [OK] Inserted: Tanzania’s poll unrest has 'stained' the country's ... [topic=politics] [sentiment=negative] [image=yes]
   ```
5. Schedule via cron/Task Scheduler/systemd for continuous ingestion.

## Streamlit Frontend
- Reads `BACKEND_URL` from `.env` (defaults to `http://localhost:8000`).  
- Sidebar filters: category dropdown, number of news, keyword search.  
- Each card displays image, metadata, AI summary, and link to original article.  
- Works with both light (email-style) and dark UI themes (see screenshots above).

## Environment Variables
`.env` (repo root) is loaded by both backend and frontend.

| Variable | Purpose | Example |
|----------|---------|---------|
| `DATABASE_URL` | SQLAlchemy connection string | `postgresql://postgres:password@localhost:5432/news_aggregator` |
| `OLLAMA_BASE_URL` | Ollama server | `http://localhost:11434` |
| `OLLAMA_MODEL` | Model name | `llama3.1` |
| `BACKEND_HOST` | Internal URL (e.g., Docker networking) | `http://backend:8000` |
| `BACKEND_URL` | Streamlit access URL | `http://localhost:8000` |

## Development Tips
- When adjusting models, run Alembic migrations (not yet included) or manually adjust tables.  
- Logging from ingestion helps spot malformed feeds or scraping failures—capture logs centrally if running in production.  
- To extend summarization rules, edit `backend/config.py` (prompt, model options, fallback behavior).  
- Add more feeds by extending `RSS_SOURCES` or reading from a DB/config service.  
- For Docker deployments, mount Ollama’s model cache and expose port `11434`.

## Roadmap Ideas
1. Add user authentication to curate personalized feeds.  
2. Introduce embedding search / semantic filters.  
3. Implement background task queue (Celery/RQ) for ingestion + summarization at scale.  
4. Add caching/CDN for article images.  
5. Provide export endpoints (email digest, Slack bot, etc.).

---

Maintained with ❤️ for data-driven newsrooms. Contributions and issue reports are welcome!

