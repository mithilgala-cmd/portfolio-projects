"""Task HTTP endpoints.

This router is intentionally thin: it handles HTTP concerns only
(request parsing, status codes, responses) and delegates all
business logic to ``src.services.task_service``.
"""

from typing import Optional

from fastapi import APIRouter, Query, Response, status

from src.models import (
    PaginatedResponse,
    Task,
    TaskCreate,
    TaskPriority,
    TaskStatus,
    TaskStatusUpdate,
    TaskUpdate,
)
from src.services import task_service

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=PaginatedResponse[Task], summary="List tasks")
def list_tasks(
    status: Optional[TaskStatus] = Query(default=None, description="Filter by status"),
    priority: Optional[TaskPriority] = Query(default=None, description="Filter by priority"),
    page: int = Query(default=1, ge=1, description="Page number (1-indexed)"),
    size: int = Query(default=20, ge=1, le=100, description="Items per page"),
) -> PaginatedResponse[Task]:
    """Return a paginated list of tasks with optional status and priority filters."""
    return task_service.list_tasks(status=status, priority=priority, page=page, size=size)


@router.get("/{task_id}", response_model=Task, summary="Get task")
def get_task(task_id: int) -> Task:
    """Return a single task by ID."""
    return task_service.get_task(task_id)


@router.post("", response_model=Task, status_code=status.HTTP_201_CREATED, summary="Create task")
def create_task(payload: TaskCreate) -> Task:
    """Create a new task."""
    return task_service.create_task(payload)


@router.patch("/{task_id}", response_model=Task, summary="Update task")
def update_task(task_id: int, payload: TaskUpdate) -> Task:
    """Partially update a task's title, description, and/or priority."""
    return task_service.update_task(task_id, payload)


@router.patch("/{task_id}/status", response_model=Task, summary="Update task status")
def update_task_status(task_id: int, payload: TaskStatusUpdate) -> Task:
    """Move a task through its status workflow."""
    return task_service.update_task_status(task_id, payload)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete task")
def delete_task(task_id: int) -> Response:
    """Permanently delete a task."""
    task_service.delete_task(task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
