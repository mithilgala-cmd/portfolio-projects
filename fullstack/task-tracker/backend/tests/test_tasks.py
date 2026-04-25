"""Tests for task endpoints.

All tests use the in_memory store (forced by conftest.py) so no
external services are needed.
"""

import pytest
from fastapi.testclient import TestClient

from src.main import app
from src.store import task_store

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_store() -> None:
    task_store.clear()
    yield
    task_store.clear()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _create(title: str = "Test task", priority: str = "medium") -> dict:
    r = client.post("/tasks", json={"title": title, "priority": priority})
    assert r.status_code == 201
    return r.json()


def _list(**params) -> dict:
    r = client.get("/tasks", params=params)
    assert r.status_code == 200
    return r.json()


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------

def test_create_task_returns_201() -> None:
    data = _create("Write README")
    assert data["id"] == 1
    assert data["title"] == "Write README"
    assert data["status"] == "todo"
    assert data["priority"] == "medium"


def test_create_task_with_priority() -> None:
    data = _create("Urgent fix", priority="high")
    assert data["priority"] == "high"


def test_create_task_empty_title_rejected() -> None:
    r = client.post("/tasks", json={"title": ""})
    assert r.status_code == 422


def test_create_task_title_too_long_rejected() -> None:
    r = client.post("/tasks", json={"title": "x" * 121})
    assert r.status_code == 422


# ---------------------------------------------------------------------------
# List / pagination
# ---------------------------------------------------------------------------

def test_list_returns_paginated_response() -> None:
    _create("A")
    _create("B")
    data = _list()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "pages" in data
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_list_pagination() -> None:
    for i in range(5):
        _create(f"Task {i}")
    page1 = _list(page=1, size=3)
    page2 = _list(page=2, size=3)
    assert len(page1["items"]) == 3
    assert len(page2["items"]) == 2
    assert page1["total"] == 5
    assert page1["pages"] == 2


# ---------------------------------------------------------------------------
# Filtering
# ---------------------------------------------------------------------------

def test_filter_tasks_by_status() -> None:
    task = _create("Task A")
    client.patch(f"/tasks/{task['id']}/status", json={"status": "in_progress"})
    _create("Task B")  # stays todo

    in_prog = _list(status="in_progress")
    todo = _list(status="todo")

    assert len(in_prog["items"]) == 1
    assert in_prog["items"][0]["title"] == "Task A"
    assert len(todo["items"]) == 1
    assert todo["items"][0]["title"] == "Task B"


def test_filter_tasks_by_priority() -> None:
    _create("High task", priority="high")
    _create("Low task", priority="low")

    highs = _list(priority="high")
    lows = _list(priority="low")

    assert len(highs["items"]) == 1
    assert highs["items"][0]["title"] == "High task"
    assert len(lows["items"]) == 1


def test_filter_by_status_and_priority() -> None:
    t1 = _create("High todo", priority="high")
    t2 = _create("High done", priority="high")
    client.patch(f"/tasks/{t2['id']}/status", json={"status": "done"})

    result = _list(status="todo", priority="high")
    assert result["total"] == 1
    assert result["items"][0]["id"] == t1["id"]


# ---------------------------------------------------------------------------
# Get single
# ---------------------------------------------------------------------------

def test_get_single_task_returns_200() -> None:
    task = _create("Solo task")
    r = client.get(f"/tasks/{task['id']}")
    assert r.status_code == 200
    assert r.json()["title"] == "Solo task"


def test_get_missing_task_returns_404() -> None:
    assert client.get("/tasks/999").status_code == 404


# ---------------------------------------------------------------------------
# Update (PATCH /tasks/{id})
# ---------------------------------------------------------------------------

def test_update_task_title() -> None:
    task = _create("Old title")
    r = client.patch(f"/tasks/{task['id']}", json={"title": "New title"})
    assert r.status_code == 200
    assert r.json()["title"] == "New title"


def test_update_task_description() -> None:
    task = _create("Task")
    r = client.patch(f"/tasks/{task['id']}", json={"description": "Updated desc"})
    assert r.status_code == 200
    assert r.json()["description"] == "Updated desc"


def test_update_task_priority() -> None:
    task = _create("Task", priority="low")
    r = client.patch(f"/tasks/{task['id']}", json={"priority": "high"})
    assert r.status_code == 200
    assert r.json()["priority"] == "high"


def test_update_missing_task_returns_404() -> None:
    assert client.patch("/tasks/999", json={"title": "Ghost"}).status_code == 404


# ---------------------------------------------------------------------------
# Status update (PATCH /tasks/{id}/status)
# ---------------------------------------------------------------------------

def test_update_status_changes_task() -> None:
    task = _create("Task two")
    r = client.patch(f"/tasks/{task['id']}/status", json={"status": "in_progress"})
    assert r.status_code == 200
    assert r.json()["status"] == "in_progress"


def test_update_status_missing_task_returns_404() -> None:
    assert client.patch("/tasks/999/status", json={"status": "done"}).status_code == 404


def test_update_status_invalid_value_rejected() -> None:
    task = _create("Task")
    assert client.patch(f"/tasks/{task['id']}/status", json={"status": "flying"}).status_code == 422


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------

def test_delete_task_returns_204() -> None:
    task = _create("Task three")
    r = client.delete(f"/tasks/{task['id']}")
    assert r.status_code == 204
    assert _list()["total"] == 0


def test_delete_missing_task_returns_404() -> None:
    assert client.delete("/tasks/999").status_code == 404
