"""Supabase client factory.

Keeps database connection concerns out of the store layer.
The client is built once at import time via get_client(); callers
should treat it as a read-only singleton.
"""

from __future__ import annotations

import logging
from typing import Any

from src import config

logger = logging.getLogger(__name__)

try:
    from supabase import Client, create_client as _create_client
except ImportError:  # pragma: no cover
    Client = Any  # type: ignore[assignment,misc]
    _create_client = None  # type: ignore[assignment]

_client: "Client | None" = None


def get_client() -> "Client | None":
    """Return a cached Supabase client, or None if credentials are missing."""
    global _client
    if _client is not None:
        return _client

    if _create_client is None:
        logger.warning("supabase package is not installed.")
        return None

    if not config.SUPABASE_URL or not config.SUPABASE_KEY:
        logger.warning("Supabase credentials not configured (SUPABASE_URL / SUPABASE_KEY).")
        return None

    try:
        _client = _create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
        logger.info("Supabase client initialised (%s)", config.SUPABASE_URL)
    except Exception as exc:  # pragma: no cover
        logger.exception("Failed to create Supabase client: %s", exc)
        return None

    return _client
