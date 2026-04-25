"""
routers/news.py — News endpoints: top headlines, search, sources.

All responses are cached with TTL defined in config.yml.
"""

import logging
from typing import List, Optional

from fastapi import APIRouter, Query

from src import cache, config, fetcher
from src.models import Article, NewsResponse, NewsSource, Source, SourcesResponse

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/news", tags=["News"])


def _parse_articles(raw_articles: list) -> List[Article]:
    """Convert raw NewsAPI article dicts into Article Pydantic models."""
    articles = []
    for item in raw_articles:
        articles.append(
            Article(
                source=Source(
                    id=item.get("source", {}).get("id"),
                    name=item.get("source", {}).get("name", "Unknown"),
                ),
                author=item.get("author"),
                title=item.get("title", ""),
                description=item.get("description"),
                url=item.get("url", ""),
                url_to_image=item.get("urlToImage"),
                published_at=item.get("publishedAt"),
                content=item.get("content"),
            )
        )
    return articles


# ── Top Headlines ──────────────────────────────────────────────────────

@router.get(
    "/top-headlines",
    response_model=NewsResponse,
    summary="Get Top Headlines",
)
async def top_headlines(
    country: str = Query(
        default=config.DEFAULT_COUNTRY,
        description="2-letter ISO 3166-1 country code (e.g. us, gb, in)",
    ),
    category: Optional[str] = Query(
        default=None,
        description="Category: business, entertainment, general, health, science, sports, technology",
    ),
    page_size: int = Query(
        default=config.DEFAULT_PAGE_SIZE,
        ge=1,
        le=config.MAX_PAGE_SIZE,
        description="Number of articles to return (max 20)",
    ),
) -> NewsResponse:
    """
    Fetch the top headlines for a given country and optional category.
    Results are cached for the TTL configured in config.yml.
    """
    cache_key = f"headlines::{country}::{category}::{page_size}"
    cached = cache.get(cache_key)
    if cached:
        return NewsResponse(**cached, cached=True)

    data = await fetcher.fetch_top_headlines(country=country, category=category, page_size=page_size)
    articles = _parse_articles(data.get("articles", []))

    result = {
        "status": data.get("status", "ok"),
        "total_results": data.get("totalResults", 0),
        "articles": [a.model_dump() for a in articles],
    }
    cache.set(cache_key, result)
    return NewsResponse(**result, cached=False)


# ── Search ─────────────────────────────────────────────────────────────

@router.get(
    "/search",
    response_model=NewsResponse,
    summary="Search News Articles",
)
async def search_news(
    q: str = Query(..., description="Keyword(s) to search for in news articles"),
    language: str = Query(
        default=config.DEFAULT_LANGUAGE,
        description="2-letter ISO-639-1 language code (e.g. en, fr, de)",
    ),
    sort_by: str = Query(
        default="publishedAt",
        description="Sort order: relevancy | popularity | publishedAt",
    ),
    page_size: int = Query(
        default=config.DEFAULT_PAGE_SIZE,
        ge=1,
        le=config.MAX_PAGE_SIZE,
        description="Number of articles to return (max 20)",
    ),
) -> NewsResponse:
    """
    Search for news articles matching a keyword query.
    Results are cached for the TTL configured in config.yml.
    """
    cache_key = f"search::{q}::{language}::{sort_by}::{page_size}"
    cached = cache.get(cache_key)
    if cached:
        return NewsResponse(**cached, cached=True)

    data = await fetcher.fetch_search(q=q, language=language, sort_by=sort_by, page_size=page_size)
    articles = _parse_articles(data.get("articles", []))

    result = {
        "status": data.get("status", "ok"),
        "total_results": data.get("totalResults", 0),
        "articles": [a.model_dump() for a in articles],
    }
    cache.set(cache_key, result)
    return NewsResponse(**result, cached=False)


# ── Sources ────────────────────────────────────────────────────────────

@router.get(
    "/sources",
    response_model=SourcesResponse,
    summary="List News Sources",
)
async def list_sources(
    category: Optional[str] = Query(
        default=None,
        description="Filter by category (e.g. technology, sports)",
    ),
    language: Optional[str] = Query(
        default=None,
        description="Filter by language (e.g. en)",
    ),
    country: Optional[str] = Query(
        default=None,
        description="Filter by country (e.g. us)",
    ),
) -> SourcesResponse:
    """
    List available news sources, optionally filtered by category, language, or country.
    Results are cached for the TTL configured in config.yml.
    """
    cache_key = f"sources::{category}::{language}::{country}"
    cached = cache.get(cache_key)
    if cached:
        return SourcesResponse(**cached, cached=True)

    data = await fetcher.fetch_sources(category=category, language=language, country=country)
    sources = [
        NewsSource(
            id=s.get("id", ""),
            name=s.get("name", ""),
            description=s.get("description", ""),
            url=s.get("url", ""),
            category=s.get("category", ""),
            language=s.get("language", ""),
            country=s.get("country", ""),
        )
        for s in data.get("sources", [])
    ]

    result = {
        "status": data.get("status", "ok"),
        "sources": [s.model_dump() for s in sources],
    }
    cache.set(cache_key, result)
    return SourcesResponse(**result, cached=False)
