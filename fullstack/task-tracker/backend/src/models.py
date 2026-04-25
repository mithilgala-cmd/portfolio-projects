"""Pydantic models for tasks."""

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class TaskStatus(str, Enum):
    """Valid task lifecycle states."""

    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"


class TaskPriority(str, Enum):
    """Task urgency levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskCreate(BaseModel):
    """Payload for creating a task."""

    title: str = Field(..., min_length=1, max_length=120)
    description: str = Field(default="", max_length=500)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)


class TaskUpdate(BaseModel):
    """Payload for partial task update (title, description, priority)."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    priority: Optional[TaskPriority] = None


class TaskStatusUpdate(BaseModel):
    """Payload for updating task status."""

    status: TaskStatus


class Task(BaseModel):
    """Task response model."""

    id: int
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime
