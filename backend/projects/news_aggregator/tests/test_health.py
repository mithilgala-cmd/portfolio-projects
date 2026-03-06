"""
tests/test_health.py — Tests for the /health endpoint.
"""

import pytest
from fastapi.testclient import TestClient

from src.main import app

client = TestClient(app)


def test_health_returns_200():
    response = client.get("/health")
    assert response.status_code == 200


def test_health_response_structure():
    response = client.get("/health")
    data = response.json()
    assert "status" in data
    assert "version" in data
    assert "newsapi_key_configured" in data
    assert "timestamp" in data


def test_health_status_is_ok():
    response = client.get("/health")
    assert response.json()["status"] == "ok"


def test_root_returns_200():
    response = client.get("/")
    assert response.status_code == 200


def test_root_has_docs_key():
    response = client.get("/")
    assert "docs" in response.json()
