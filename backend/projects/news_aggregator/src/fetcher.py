"""
fetcher.py — Async HTTP client for NewsAPI.org.

All functions use httpx.AsyncClient to make non-blocking requests.
Raises HTTPException on API errors so FastAPI returns proper JSON errors.
"""

import logging
from typing import Any, Dict, Optional

import httpx
from fastapi import HTTPException

from src import config

logger = logging.getLogger(__name__)

# Shared async client (created once, reused across requests)
_client: Optional[httpx.AsyncClient] = None


def get_client() -> httpx.AsyncClient:
    global _client
    if _client is None or _client.is_closed:
        _client = httpx.AsyncClient(timeout=10.0)
    return _client


async def close_client() -> None:
    global _client
    if _client and not _client.is_closed:
        await _client.aclose()
        _client = None


def _check_api_key() -> None:
    if not config.NEWSAPI_KEY:
        raise HTTPException(
            status_code=503,
            detail=(
                "NEWS_API_KEY is not configured. "
                "Please copy .env.example to .env and add your key."
            ),
        )


async def _get(endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
    """Internal helper: send GET to NewsAPI, return parsed JSON."""
    _check_api_key()
    params["apiKey"] = config.NEWSAPI_KEY
    url = f"{config.NEWSAPI_BASE_URL}/{endpoint}"

    logger.info(f"Fetching NewsAPI [{endpoint}] params={params}")
    client = get_client()
    try:
        response = await client.get(url, params=params)
    except httpx.RequestError as exc:
        logger.error(f"Network error calling NewsAPI: {exc}")
        raise HTTPException(status_code=503, detail=f"NewsAPI unreachable: {exc}")

    if response.status_code == 401:
        raise HTTPException(status_code=401, detail="Invalid NewsAPI key.")
    if response.status_code == 429:
        raise HTTPException(status_code=429, detail="NewsAPI rate limit exceeded. Try again later.")
    if response.status_code != 200:
        raise HTTPException(
            status_code=502,
            detail=f"NewsAPI returned {response.status_code}: {response.text}",
        )

    data = response.json()
    if data.get("status") != "ok":
        raise HTTPException(status_code=502, detail=data.get("message", "Unknown NewsAPI error."))

    return data


async def fetch_top_headlines(
    country: str,
    category: Optional[str],
    page_size: int,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {
        "country": country,
        "pageSize": page_size,
    }
    if category:
        params["category"] = category
    return await _get("top-headlines", params)


async def fetch_search(
    q: str,
    language: str,
    sort_by: str,
    page_size: int,
) -> Dict[str, Any]:
    params: Dict[str, Any] = {
        "q": q,
        "language": language,
        "sortBy": sort_by,
        "pageSize": page_size,
    }
    return await _get("everything", params)


async def fetch_sources(
    category: Optional[str],
    language: Optional[str],
    country: Optional[str],
) -> Dict[str, Any]:
    params: Dict[str, Any] = {}
    if category:
        params["category"] = category
    if language:
        params["language"] = language
    if country:
        params["country"] = country
    return await _get("top-headlines/sources", params)
