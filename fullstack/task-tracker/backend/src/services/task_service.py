"""Task business-logic service.

This layer sits between HTTP routers and the storage layer.
Routers own request/response translation; this module owns
domain rules, validation-beyond-schema, and pagination maths.
"""

from __future__ import annotations

import logging
import math

from fastapi import HTTPException, status

from src.models import (
    PaginatedResponse,
    Task,
    TaskCreate,
    TaskPriority,
    TaskStatus,
    TaskStatusUpdate,
    TaskUpdate,
)
from src.store import task_store

logger = logging.getLogger(__name__)

_MAX_PAGE_SIZE = 100


def list_tasks(
    *,
    status: TaskStatus | None = None,
    priority: TaskPriority | None = None,
    page: int = 1,
    size: int = 20,
) -> PaginatedResponse[Task]:
    """Return a paginated, optionally-filtered list of tasks."""
    if page < 1:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="page must be >= 1")
    if not (1 <= size <= _MAX_PAGE_SIZE):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"size must be between 1 and {_MAX_PAGE_SIZE}",
        )

    skip = (page - 1) * size
    items, total = task_store.list_tasks(status=status, priority=priority, skip=skip, limit=size)
    pages = math.ceil(total / size) if total > 0 else 1

    logger.debug("list_tasks status=%s priority=%s page=%d size=%d → %d/%d", status, priority, page, size, len(items), total)
    return PaginatedResponse(items=items, total=total, page=page, size=size, pages=pages)


def get_task(task_id: int) -> Task:
    """Return a single task or raise 404."""
    task = task_store.get_task(task_id)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    return task


def create_task(payload: TaskCreate) -> Task:
    """Create and return a new task."""
    task = task_store.create_task(payload)
    logger.info("Task created id=%d title=%r priority=%s", task.id, task.title, task.priority)
    return task


def update_task(task_id: int, payload: TaskUpdate) -> Task:
    """Apply a partial update; raise 404 if missing."""
    task = task_store.update_task(task_id=task_id, payload=payload)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    logger.info("Task updated id=%d", task_id)
    return task


def update_task_status(task_id: int, payload: TaskStatusUpdate) -> Task:
    """Update status only; raise 404 if missing."""
    task = task_store.update_status(task_id=task_id, status=payload.status)
    if task is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    logger.info("Task %d status → %s", task_id, payload.status)
    return task


def delete_task(task_id: int) -> None:
    """Delete a task; raise 404 if not found."""
    deleted = task_store.delete_task(task_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Task {task_id} not found")
    logger.info("Task deleted id=%d", task_id)
