"""
models.py — Pydantic schemas for API responses.
"""

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, HttpUrl


class Source(BaseModel):
    id: Optional[str] = None
    name: str


class Article(BaseModel):
    source: Source
    author: Optional[str] = None
    title: str
    description: Optional[str] = None
    url: str
    url_to_image: Optional[str] = None
    published_at: Optional[str] = None
    content: Optional[str] = None


class NewsResponse(BaseModel):
    status: str
    total_results: int
    cached: bool = False
    articles: List[Article]


class NewsSource(BaseModel):
    id: str
    name: str
    description: str
    url: str
    category: str
    language: str
    country: str


class SourcesResponse(BaseModel):
    status: str
    cached: bool = False
    sources: List[NewsSource]


class HealthResponse(BaseModel):
    status: str
    version: str
    newsapi_key_configured: bool
    timestamp: str
