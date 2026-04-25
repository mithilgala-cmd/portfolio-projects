"""Pydantic models for tasks."""

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Valid task lifecycle states."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskCreate(BaseModel):
    """Payload for creating a task."""

    title: str = Field(..., min_length=1, max_length=120)
    description: str = Field(default="", max_length=500)


class TaskStatusUpdate(BaseModel):
    """Payload for updating task status."""

    status: TaskStatus


class Task(BaseModel):
    """Task response model."""

    id: int
    title: str
    description: str
    status: TaskStatus
    created_at: datetime
    updated_at: datetime
