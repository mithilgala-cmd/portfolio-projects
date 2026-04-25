"""Pydantic models / schemas for tasks."""

from datetime import datetime
from enum import Enum
from typing import Generic, Optional, TypeVar

from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------

class TaskCreate(BaseModel):
    """Payload for creating a task."""

    title: str = Field(..., min_length=1, max_length=120, examples=["Fix login bug"])
    description: str = Field(default="", max_length=500, examples=["Investigate OAuth callback"])
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM)


class TaskUpdate(BaseModel):
    """Payload for partial task update (all fields optional)."""

    title: Optional[str] = Field(default=None, min_length=1, max_length=120)
    description: Optional[str] = Field(default=None, max_length=500)
    priority: Optional[TaskPriority] = None


class TaskStatusUpdate(BaseModel):
    """Payload for updating task status only."""

    status: TaskStatus


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------

class Task(BaseModel):
    """Full task response model."""

    id: int
    title: str
    description: str
    status: TaskStatus
    priority: TaskPriority
    created_at: datetime
    updated_at: datetime


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated list wrapper."""

    items: list[T]
    total: int
    page: int
    size: int
    pages: int
