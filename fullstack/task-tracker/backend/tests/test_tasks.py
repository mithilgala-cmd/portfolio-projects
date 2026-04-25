"""Tests for task endpoints."""

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


def test_create_task_returns_201() -> None:
    response = client.post("/tasks", json={"title": "Write README", "description": "Project notes"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Write README"
    assert data["status"] == "todo"


def test_list_tasks_contains_created_task() -> None:
    client.post("/tasks", json={"title": "Task one", "description": ""})
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Task one"


def test_update_status_changes_task() -> None:
    created = client.post("/tasks", json={"title": "Task two", "description": ""}).json()
    response = client.patch(f"/tasks/{created['id']}/status", json={"status": "in_progress"})
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"


def test_delete_task_returns_204() -> None:
    created = client.post("/tasks", json={"title": "Task three", "description": ""}).json()
    response = client.delete(f"/tasks/{created['id']}")
    assert response.status_code == 204
    assert client.get("/tasks").json() == []


def test_update_missing_task_returns_404() -> None:
    response = client.patch("/tasks/999/status", json={"status": "done"})
    assert response.status_code == 404


def test_delete_missing_task_returns_404() -> None:
    response = client.delete("/tasks/999")
    assert response.status_code == 404
