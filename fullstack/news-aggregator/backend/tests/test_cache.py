"""
tests/test_cache.py — Unit tests for the bounded in-memory cache.
"""

import time
import pytest
from unittest.mock import patch

from src import cache
from src import config

@pytest.fixture(autouse=True)
def clear_cache_before_each():
    cache.clear()
    yield
    cache.clear()

def test_cache_set_and_get():
    # Test normal set/get functionality
    cache.set("key1", "val1")
    assert cache.get("key1") == "val1"
    assert cache.size() == 1

def test_cache_ttl_expiration():
    # Mock time.time() to simulate TTL expiration
    with patch("src.cache.time.time") as mock_time:
        mock_time.return_value = 100.0
        cache.set("key1", "val1")
        
        # Advance time by less than TTL
        mock_time.return_value = 100.0 + config.CACHE_TTL_SECONDS - 1.0
        assert cache.get("key1") == "val1"
        
        # Advance time past TTL
        mock_time.return_value = 100.0 + config.CACHE_TTL_SECONDS + 1.0
        assert cache.get("key1") is None
        assert cache.size() == 0

def test_cache_max_size_eviction():
    # Test that adding an item past MAX_CACHE_SIZE evicts the oldest entry
    with patch("src.cache.MAX_CACHE_SIZE", 2):
        cache.set("key1", "val1")
        cache.set("key2", "val2")
        assert cache.get("key1") == "val1"
        assert cache.get("key2") == "val2"
        assert cache.size() == 2

        # Adding 3rd item should evict key1
        cache.set("key3", "val3")
        assert cache.size() == 2
        assert cache.get("key1") is None
        assert cache.get("key2") == "val2"
        assert cache.get("key3") == "val3"

def test_cache_key_update_does_not_evict():
    # Test that updating an existing key doesn't trigger Max Size eviction incorrectly
    with patch("src.cache.MAX_CACHE_SIZE", 2):
        cache.set("key1", "val1")
        cache.set("key2", "val2")
        
        # Update key1
        cache.set("key1", "val1_updated")
        assert cache.size() == 2
        
        # Adding new item key3 evicts key2 instead of key1 since key1 was recently updated
        cache.set("key3", "val3")
        assert cache.size() == 2
        
        assert cache.get("key1") == "val1_updated"
        assert cache.get("key2") is None
        assert cache.get("key3") == "val3"

def test_cache_clear():
    cache.set("k1", "v1")
    cache.set("k2", "v2")
    cache.clear()
    assert cache.size() == 0
    assert cache.get("k1") is None
