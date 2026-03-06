"""
cache.py — Simple in-memory TTL cache.

Stores results keyed by query string. Entries expire after CACHE_TTL_SECONDS.
Thread-safe for single-process async use (no locking needed with asyncio).
"""

import logging
import time
from typing import Any, Optional, Tuple

from src.config import CACHE_TTL_SECONDS

logger = logging.getLogger(__name__)

# Internal store: { key: (stored_at_timestamp, data) }
_store: dict[str, Tuple[float, Any]] = {}


def get(key: str) -> Optional[Any]:
    """Return cached data for key if not expired, else None."""
    if key not in _store:
        return None
    stored_at, data = _store[key]
    age = time.time() - stored_at
    if age > CACHE_TTL_SECONDS:
        logger.debug(f"Cache EXPIRED for key: {key!r} (age={age:.1f}s)")
        del _store[key]
        return None
    logger.debug(f"Cache HIT for key: {key!r} (age={age:.1f}s)")
    return data


def set(key: str, data: Any) -> None:
    """Store data in cache with current timestamp."""
    logger.debug(f"Cache SET for key: {key!r}")
    _store[key] = (time.time(), data)


def clear() -> None:
    """Clear all cached entries (useful for testing)."""
    _store.clear()


def size() -> int:
    """Return number of entries currently in the cache."""
    return len(_store)
