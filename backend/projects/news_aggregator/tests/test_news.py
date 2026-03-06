"""
tests/test_news.py — Tests for /news endpoints using mocked NewsAPI responses.

Uses unittest.mock to patch fetcher functions so no real HTTP calls are made.
"""

import pytest
from unittest.mock import AsyncMock, patch
from fastapi.testclient import TestClient

from src.main import app
from src import cache

client = TestClient(app)

# ── Fake NewsAPI payloads ──────────────────────────────────────────────

FAKE_HEADLINES_RESPONSE = {
    "status": "ok",
    "totalResults": 2,
    "articles": [
        {
            "source": {"id": "bbc-news", "name": "BBC News"},
            "author": "BBC",
            "title": "Test Headline 1",
            "description": "A description",
            "url": "https://bbc.com/news/1",
            "urlToImage": None,
            "publishedAt": "2024-01-01T12:00:00Z",
            "content": "Full content here.",
        },
        {
            "source": {"id": None, "name": "CNN"},
            "author": None,
            "title": "Test Headline 2",
            "description": None,
            "url": "https://cnn.com/news/2",
            "urlToImage": "https://cnn.com/img.jpg",
            "publishedAt": "2024-01-01T11:00:00Z",
            "content": None,
        },
    ],
}

FAKE_SEARCH_RESPONSE = {
    "status": "ok",
    "totalResults": 1,
    "articles": [
        {
            "source": {"id": "techcrunch", "name": "TechCrunch"},
            "author": "Author",
            "title": "Python Reaches New Heights",
            "description": "Python is everywhere.",
            "url": "https://techcrunch.com/python",
            "urlToImage": None,
            "publishedAt": "2024-01-02T09:00:00Z",
            "content": "Content.",
        }
    ],
}

FAKE_SOURCES_RESPONSE = {
    "status": "ok",
    "sources": [
        {
            "id": "bbc-news",
            "name": "BBC News",
            "description": "British Broadcasting Corporation",
            "url": "https://bbc.com",
            "category": "general",
            "language": "en",
            "country": "gb",
        }
    ],
}


# ── Setup/teardown ─────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def clear_cache_before_each():
    """Clear the in-memory cache before each test to prevent bleed-over."""
    cache.clear()
    yield
    cache.clear()


# ── Top Headlines ──────────────────────────────────────────────────────

@patch("src.routers.news.fetcher.fetch_top_headlines", new_callable=AsyncMock)
def test_top_headlines_returns_200(mock_fetch):
    mock_fetch.return_value = FAKE_HEADLINES_RESPONSE
    response = client.get("/news/top-headlines")
    assert response.status_code == 200


@patch("src.routers.news.fetcher.fetch_top_headlines", new_callable=AsyncMock)
def test_top_headlines_response_structure(mock_fetch):
    mock_fetch.return_value = FAKE_HEADLINES_RESPONSE
    data = client.get("/news/top-headlines").json()
    assert "status" in data
    assert "total_results" in data
    assert "articles" in data
    assert isinstance(data["articles"], list)


@patch("src.routers.news.fetcher.fetch_top_headlines", new_callable=AsyncMock)
def test_top_headlines_article_fields(mock_fetch):
    mock_fetch.return_value = FAKE_HEADLINES_RESPONSE
    articles = client.get("/news/top-headlines").json()["articles"]
    assert len(articles) == 2
    assert articles[0]["title"] == "Test Headline 1"
    assert articles[0]["source"]["name"] == "BBC News"


@patch("src.routers.news.fetcher.fetch_top_headlines", new_callable=AsyncMock)
def test_top_headlines_uses_cache_on_second_call(mock_fetch):
    mock_fetch.return_value = FAKE_HEADLINES_RESPONSE
    client.get("/news/top-headlines")
    client.get("/news/top-headlines")
    # Fetcher should only be called once (second call hits cache)
    assert mock_fetch.call_count == 1


# ── Search ─────────────────────────────────────────────────────────────

@patch("src.routers.news.fetcher.fetch_search", new_callable=AsyncMock)
def test_search_returns_200(mock_fetch):
    mock_fetch.return_value = FAKE_SEARCH_RESPONSE
    response = client.get("/news/search?q=python")
    assert response.status_code == 200


@patch("src.routers.news.fetcher.fetch_search", new_callable=AsyncMock)
def test_search_missing_q_returns_422(mock_fetch):
    """q is required; missing it should return 422 Unprocessable Entity."""
    response = client.get("/news/search")
    assert response.status_code == 422


@patch("src.routers.news.fetcher.fetch_search", new_callable=AsyncMock)
def test_search_returns_articles(mock_fetch):
    mock_fetch.return_value = FAKE_SEARCH_RESPONSE
    data = client.get("/news/search?q=python").json()
    assert data["total_results"] == 1
    assert data["articles"][0]["title"] == "Python Reaches New Heights"


# ── Sources ────────────────────────────────────────────────────────────

@patch("src.routers.news.fetcher.fetch_sources", new_callable=AsyncMock)
def test_sources_returns_200(mock_fetch):
    mock_fetch.return_value = FAKE_SOURCES_RESPONSE
    response = client.get("/news/sources")
    assert response.status_code == 200


@patch("src.routers.news.fetcher.fetch_sources", new_callable=AsyncMock)
def test_sources_response_structure(mock_fetch):
    mock_fetch.return_value = FAKE_SOURCES_RESPONSE
    data = client.get("/news/sources").json()
    assert "sources" in data
    assert data["sources"][0]["name"] == "BBC News"
