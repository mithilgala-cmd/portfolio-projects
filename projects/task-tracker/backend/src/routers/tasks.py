"""Task CRUD endpoints."""

from fastapi import APIRouter, HTTPException, Response, status

from src.models import Task, TaskCreate, TaskStatusUpdate
from src.store import task_store

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[Task])
def list_tasks() -> list[Task]:
    """Return all tasks."""
    return task_store.list_tasks()


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreate) -> Task:
    """Create a task."""
    return task_store.create_task(payload)


@router.patch("/{task_id}/status", response_model=Task)
def update_task_status(task_id: int, payload: TaskStatusUpdate) -> Task:
    """Update the status for a task."""
    task = task_store.update_status(task_id=task_id, status=payload.status)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int) -> Response:
    """Delete a task."""
    deleted = task_store.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
