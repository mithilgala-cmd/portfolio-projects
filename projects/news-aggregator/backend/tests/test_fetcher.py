"""
tests/test_fetcher.py — Unit tests for the fetcher logic (error handling, param building).
"""

import pytest
from unittest.mock import AsyncMock, patch
import httpx
from fastapi import HTTPException

from src import fetcher
from src import config

@pytest.fixture(autouse=True)
def unconfigure_api_key(monkeypatch):
    """Ensure tests start with or without key based on test requirement."""
    monkeypatch.setattr(config, "NEWSAPI_KEY", "dummy-key")

@pytest.mark.asyncio
async def test_no_api_key_raises_503(monkeypatch):
    monkeypatch.setattr(config, "NEWSAPI_KEY", "")
    with pytest.raises(HTTPException) as exc:
        await fetcher.fetch_top_headlines("us", None, 10)
    assert exc.value.status_code == 503
    assert "not configured" in exc.value.detail

@pytest.mark.asyncio
@patch("src.fetcher.get_client")
async def test_network_error_raises_503(mock_get_client):
    mock_client = AsyncMock()
    mock_client.get.side_effect = httpx.RequestError("Network error")
    mock_get_client.return_value = mock_client

    with pytest.raises(HTTPException) as exc:
        await fetcher.fetch_top_headlines("us", None, 10)
    assert exc.value.status_code == 503
    assert "NewsAPI unreachable" in exc.value.detail

@pytest.mark.asyncio
@patch("src.fetcher.get_client")
async def test_api_unauthorized_raises_401(mock_get_client):
    mock_client = AsyncMock()
    mock_response = httpx.Response(401, json={"message": "Invalid API key"})
    mock_client.get.return_value = mock_response
    mock_get_client.return_value = mock_client

    with pytest.raises(HTTPException) as exc:
        await fetcher.fetch_top_headlines("us", None, 10)
    assert exc.value.status_code == 401
    assert "Invalid NewsAPI key" in exc.value.detail

@pytest.mark.asyncio
@patch("src.fetcher.get_client")
async def test_api_rate_limit_raises_429(mock_get_client):
    mock_client = AsyncMock()
    mock_response = httpx.Response(429, json={"message": "Rate limited"})
    mock_client.get.return_value = mock_response
    mock_get_client.return_value = mock_client

    with pytest.raises(HTTPException) as exc:
        await fetcher.fetch_top_headlines("us", None, 10)
    assert exc.value.status_code == 429
    assert "rate limit exceeded" in exc.value.detail

@pytest.mark.asyncio
@patch("src.fetcher.get_client")
async def test_api_bad_gateway_or_other_error(mock_get_client):
    mock_client = AsyncMock()
    mock_response = httpx.Response(500, json={"message": "Server error"})
    mock_client.get.return_value = mock_response
    mock_get_client.return_value = mock_client

    with pytest.raises(HTTPException) as exc:
        await fetcher.fetch_top_headlines("us", None, 10)
    assert exc.value.status_code == 502
    assert "NewsAPI returned 500" in exc.value.detail

@pytest.mark.asyncio
@patch("src.fetcher.get_client")
async def test_api_returns_status_error_but_200_http(mock_get_client):
    mock_client = AsyncMock()
    # E.g. NewsAPI returns 200 HTTP, but status: error in payload
    mock_response = httpx.Response(200, json={"status": "error", "message": "Custom error msg"})
    mock_client.get.return_value = mock_response
    mock_get_client.return_value = mock_client

    with pytest.raises(HTTPException) as exc:
        await fetcher.fetch_top_headlines("us", None, 10)
    assert exc.value.status_code == 502
    assert "Custom error msg" in exc.value.detail

@pytest.mark.asyncio
@patch("src.fetcher.get_client")
async def test_successful_fetch(mock_get_client):
    mock_client = AsyncMock()
    mock_response = httpx.Response(200, json={"status": "ok", "articles": []})
    mock_client.get.return_value = mock_response
    mock_get_client.return_value = mock_client

    result = await fetcher.fetch_search(q="bitcoin", language="en", sort_by="relevancy", page_size=5)
    
    assert result["status"] == "ok"
    mock_client.get.assert_called_once()
    # Verify params were passed properly
    _, kwargs = mock_client.get.call_args
    assert "params" in kwargs
    assert kwargs["params"]["q"] == "bitcoin"
