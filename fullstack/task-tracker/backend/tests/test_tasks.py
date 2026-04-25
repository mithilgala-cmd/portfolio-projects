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


# ---------------------------------------------------------------------------
# Create
# ---------------------------------------------------------------------------

def test_create_task_returns_201() -> None:
    response = client.post("/tasks", json={"title": "Write README", "description": "Project notes"})
    assert response.status_code == 201
    data = response.json()
    assert data["id"] == 1
    assert data["title"] == "Write README"
    assert data["status"] == "todo"
    assert data["priority"] == "medium"


def test_create_task_with_priority() -> None:
    response = client.post("/tasks", json={"title": "Urgent fix", "priority": "high"})
    assert response.status_code == 201
    assert response.json()["priority"] == "high"


def test_create_task_empty_title_rejected() -> None:
    response = client.post("/tasks", json={"title": "", "description": ""})
    assert response.status_code == 422


def test_create_task_title_too_long_rejected() -> None:
    response = client.post("/tasks", json={"title": "x" * 121})
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# List / Filter
# ---------------------------------------------------------------------------

def test_list_tasks_contains_created_task() -> None:
    client.post("/tasks", json={"title": "Task one", "description": ""})
    response = client.get("/tasks")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "Task one"


def test_filter_tasks_by_status() -> None:
    created = client.post("/tasks", json={"title": "Task A"}).json()
    client.patch(f"/tasks/{created['id']}/status", json={"status": "in_progress"})
    client.post("/tasks", json={"title": "Task B"})  # stays todo

    in_progress = client.get("/tasks?status=in_progress").json()
    todo = client.get("/tasks?status=todo").json()

    assert len(in_progress) == 1
    assert in_progress[0]["title"] == "Task A"
    assert len(todo) == 1
    assert todo[0]["title"] == "Task B"


# ---------------------------------------------------------------------------
# Get single
# ---------------------------------------------------------------------------

def test_get_single_task_returns_200() -> None:
    created = client.post("/tasks", json={"title": "Solo task"}).json()
    response = client.get(f"/tasks/{created['id']}")
    assert response.status_code == 200
    assert response.json()["title"] == "Solo task"


def test_get_missing_task_returns_404() -> None:
    response = client.get("/tasks/999")
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Update (PATCH /tasks/{id})
# ---------------------------------------------------------------------------

def test_update_task_title() -> None:
    created = client.post("/tasks", json={"title": "Old title"}).json()
    response = client.patch(f"/tasks/{created['id']}", json={"title": "New title"})
    assert response.status_code == 200
    assert response.json()["title"] == "New title"


def test_update_task_description() -> None:
    created = client.post("/tasks", json={"title": "Task"}).json()
    response = client.patch(f"/tasks/{created['id']}", json={"description": "Updated desc"})
    assert response.status_code == 200
    assert response.json()["description"] == "Updated desc"


def test_update_task_priority() -> None:
    created = client.post("/tasks", json={"title": "Task", "priority": "low"}).json()
    response = client.patch(f"/tasks/{created['id']}", json={"priority": "high"})
    assert response.status_code == 200
    assert response.json()["priority"] == "high"


def test_update_missing_task_returns_404() -> None:
    response = client.patch("/tasks/999", json={"title": "Ghost"})
    assert response.status_code == 404


# ---------------------------------------------------------------------------
# Status update (PATCH /tasks/{id}/status)
# ---------------------------------------------------------------------------

def test_update_status_changes_task() -> None:
    created = client.post("/tasks", json={"title": "Task two", "description": ""}).json()
    response = client.patch(f"/tasks/{created['id']}/status", json={"status": "in_progress"})
    assert response.status_code == 200
    assert response.json()["status"] == "in_progress"


def test_update_status_missing_task_returns_404() -> None:
    response = client.patch("/tasks/999/status", json={"status": "done"})
    assert response.status_code == 404


def test_update_status_invalid_value_rejected() -> None:
    created = client.post("/tasks", json={"title": "Task"}).json()
    response = client.patch(f"/tasks/{created['id']}/status", json={"status": "flying"})
    assert response.status_code == 422


# ---------------------------------------------------------------------------
# Delete
# ---------------------------------------------------------------------------

def test_delete_task_returns_204() -> None:
    created = client.post("/tasks", json={"title": "Task three", "description": ""}).json()
    response = client.delete(f"/tasks/{created['id']}")
    assert response.status_code == 204
    assert client.get("/tasks").json() == []


def test_delete_missing_task_returns_404() -> None:
    response = client.delete("/tasks/999")
    assert response.status_code == 404
