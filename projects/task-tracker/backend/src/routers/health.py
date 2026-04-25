"""Health endpoint."""

from datetime import datetime, timezone

from fastapi import APIRouter

from src import config
from src.store import task_store

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check() -> dict[str, str | bool]:
    """Return service health metadata."""
    return {
        "status": "ok",
        "version": config.APP_VERSION,
        "storage_backend": task_store.backend,
        "supabase_configured": config.supabase_is_configured(),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
