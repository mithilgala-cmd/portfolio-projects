"""
routers/health.py — Health check endpoint.
"""

from datetime import datetime, timezone

from fastapi import APIRouter

from src import config
from src.models import HealthResponse

router = APIRouter(tags=["Health"])


@router.get("/health", response_model=HealthResponse, summary="Health Check")
async def health_check() -> HealthResponse:
    """
    Returns the current health status of the API, version info,
    and whether the NewsAPI key is configured.
    """
    return HealthResponse(
        status="ok",
        version=config.APP_VERSION,
        newsapi_key_configured=bool(config.NEWSAPI_KEY),
        timestamp=datetime.now(timezone.utc).isoformat(),
    )
