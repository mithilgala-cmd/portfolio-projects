"""Task CRUD endpoints."""

from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Response, status

from src.models import Task, TaskCreate, TaskStatus, TaskStatusUpdate, TaskUpdate
from src.store import task_store

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[Task])
def list_tasks(
    status: Optional[TaskStatus] = Query(default=None, description="Filter by task status"),
) -> list[Task]:
    """Return all tasks, optionally filtered by status."""
    return task_store.list_tasks(status=status)


@router.get("/{task_id}", response_model=Task)
def get_task(task_id: int) -> Task:
    """Return a single task by ID."""
    task = task_store.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> Task:
    """Create a new task."""
    return task_store.create_task(payload)


@router.patch("/{task_id}", response_model=Task)
def update_task(task_id: int, payload: TaskUpdate) -> Task:
    """Update a task's title, description, and/or priority."""
    task = task_store.update_task(task_id=task_id, payload=payload)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.patch("/{task_id}/status", response_model=Task)
def update_task_status(task_id: int, payload: TaskStatusUpdate) -> Task:
    """Update the status for a task."""
    task = task_store.update_status(task_id=task_id, status=payload.status)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> Response:
    """Delete a task by ID."""
    deleted = task_store.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
