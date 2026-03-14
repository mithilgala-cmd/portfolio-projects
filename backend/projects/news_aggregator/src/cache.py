"""
cache.py — Simple in-memory TTL cache.

Stores results keyed by query string. Entries expire after CACHE_TTL_SECONDS.
Thread-safe for single-process async use (no locking needed with asyncio).
"""

import logging
import time
from typing import Any, Optional, Tuple

from src.config import CACHE_TTL_SECONDS, MAX_CACHE_SIZE

logger = logging.getLogger(__name__)

# Internal store: { key: (stored_at_timestamp, data) }
# In Python 3.7+, dicts preserve insertion order, making simple LRU/FIFO eviction easy.
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
    """Store data in cache with current timestamp. Evict oldest if full."""
    logger.debug(f"Cache SET for key: {key!r}")
    
    # If the key already exists, updating it just overwrites. 
    # If it's a new key and we're at capacity, we must evict the first inserted key (FIFO logic).
    while len(_store) >= MAX_CACHE_SIZE and key not in _store:
        oldest_key = next(iter(_store))
        logger.debug(f"Cache CAPACITY REACHED. Evicting oldest key: {oldest_key!r}")
        del _store[oldest_key]
        
    # Python dicts maintain insertion order. To treat this as an LRU instead of strict FIFO,
    # we could pop and re-insert on `get`. But for simple bounded caching, evicting the oldest
    # inserted item (FIFO) or the existing key when strictly at capacity is usually sufficient 
    # and keeps `get()` fast. Let's update or insert at the end.
    if key in _store:
        del _store[key] # Ensure it moves to the end of the insertion order
    _store[key] = (time.time(), data)


def clear() -> None:
    """Clear all cached entries (useful for testing)."""
    _store.clear()


def size() -> int:
    """Return number of entries currently in the cache."""
    return len(_store)
