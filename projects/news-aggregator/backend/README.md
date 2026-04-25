# News Aggregator API

A FastAPI service that fetches news from NewsAPI, validates responses, and caches results for faster repeat queries.

## Features

- Top headlines by country/category
- Keyword search endpoint
- News sources endpoint
- In-memory TTL caching
- Health endpoint
- Unit tests with mocked external calls

## Tech Stack

- Python
- FastAPI
- httpx
- Pydantic
- pytest

## Project Layout

```text
news_aggregator/
|-- src/
|   |-- main.py
|   |-- fetcher.py
|   |-- cache.py
|   |-- config.py
|   |-- models.py
|   `-- routers/
|-- tests/
|-- config.yml
|-- .env.example
`-- requirements.txt
```

## Run Locally

```bash
cd backend/projects/news_aggregator
pip install -r requirements.txt
copy .env.example .env
```

Set your `NEWS_API_KEY` inside `.env`, then run:

```bash
uvicorn src.main:app --reload --port 8000
```

Docs: `http://127.0.0.1:8000/docs`

## Test

```bash
pytest tests -v
```

## Main Endpoints

- `GET /health`
- `GET /news/top-headlines`
- `GET /news/search`
- `GET /news/sources`
