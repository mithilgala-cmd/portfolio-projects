# News Aggregator API

A RESTful backend API built with **FastAPI** that fetches, filters, and caches live news from [NewsAPI.org](https://newsapi.org). Demonstrates async HTTP, in-memory caching, Pydantic validation, and clean API design.

---

## Features

- 🔍 **Search** news articles by keyword
- 📰 **Top headlines** filtered by country and category
- 📡 **News sources** listing with filters
- ⚡ **In-memory TTL caching** — avoids redundant API calls
- ✅ **Pydantic validation** on all requests and responses
- 📄 **Auto-generated Swagger UI** at `/docs`

---

## Project Structure

```
news_aggregator/
├── src/
│   ├── main.py          # FastAPI app, CORS, lifespan
│   ├── config.py        # Config loader (.env + config.yml)
│   ├── models.py        # Pydantic response schemas
│   ├── fetcher.py       # Async httpx NewsAPI client
│   ├── cache.py         # In-memory TTL cache
│   └── routers/
│       ├── health.py    # GET /health
│       └── news.py      # GET /news/*
├── tests/
│   ├── test_health.py
│   └── test_news.py     # Mocked — no live API calls
├── .env.example
├── .gitignore
├── config.yml
└── requirements.txt
```

---

## Quick Start

### 1. Prerequisites

- Python 3.11+
- A free [NewsAPI.org](https://newsapi.org/register) API key (100 req/day on free tier)

### 2. Install dependencies

```bash
cd backend/projects/news_aggregator
pip install -r requirements.txt
```

### 3. Configure environment

```bash
copy .env.example .env
# Open .env and set: NEWS_API_KEY=your_key_here
```

### 4. Run the server

```bash
uvicorn src.main:app --reload
```

Open your browser at:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/health` | Service health check |
| `GET` | `/news/top-headlines` | Top headlines by country/category |
| `GET` | `/news/search` | Search articles by keyword |
| `GET` | `/news/sources` | List available news sources |

### `/news/top-headlines` Parameters

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `country` | string | `us` | ISO 3166-1 country code |
| `category` | string | — | business, technology, sports, health, etc. |
| `page_size` | int | `10` | Number of results (max 20) |

### `/news/search` Parameters

| Param | Type | Default | Description |
|-------|------|---------|-------------|
| `q` | string | *(required)* | Search keyword |
| `language` | string | `en` | ISO-639-1 language code |
| `sort_by` | string | `publishedAt` | relevancy \| popularity \| publishedAt |
| `page_size` | int | `10` | Number of results (max 20) |

### `/news/sources` Parameters

| Param | Type | Description |
|-------|------|-------------|
| `category` | string | Filter by category |
| `language` | string | Filter by language |
| `country` | string | Filter by country |

---

## Example Requests

```bash
# Health check
curl http://127.0.0.1:8000/health

# Top technology headlines in the US
curl "http://127.0.0.1:8000/news/top-headlines?country=us&category=technology"

# Search for Python news
curl "http://127.0.0.1:8000/news/search?q=python&sort_by=relevancy"

# List English-language sources
curl "http://127.0.0.1:8000/news/sources?language=en"
```

---

## Running Tests

```bash
pytest tests/ -v
```

Tests use `unittest.mock.AsyncMock` to patch fetcher calls — no live API hits required.

---

## Caching

All responses are cached in memory for **5 minutes** (configurable in `config.yml`). The `cached` field in each response tells you whether the result came from cache.

```json
{
  "status": "ok",
  "total_results": 38,
  "cached": true,
  "articles": [ ... ]
}
```

---

## Stack

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![httpx](https://img.shields.io/badge/httpx-async-blue?style=flat)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat&logo=pydantic&logoColor=white)

Project is still in testing phase!

Update : Tested on different devices.
Trying new features with the project.
