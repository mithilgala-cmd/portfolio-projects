"""Task storage implementations.

Two backends are provided:
  - InMemoryTaskStore  : thread-safe dict; used for local dev and all tests.
  - SupabaseTaskStore  : Postgres via the Supabase client; used in production.

The active store is selected at startup via _build_task_store() and exposed
as the module-level singleton ``task_store``.
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Protocol

from src import config
from src.db.client import get_client
from src.models import Task, TaskCreate, TaskPriority, TaskStatus, TaskUpdate

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Protocol (interface)
# ---------------------------------------------------------------------------

class TaskStoreProtocol(Protocol):
    """Contract for every task persistence layer."""

    backend: str

    def list_tasks(
        self,
        *,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> tuple[list[Task], int]:
        """Return (page_of_tasks, total_matching_count)."""

    def get_task(self, task_id: int) -> Task | None:
        """Return a single task, or None."""

    def create_task(self, payload: TaskCreate) -> Task:
        """Create and return a new task."""

    def update_task(self, task_id: int, payload: TaskUpdate) -> Task | None:
        """Partially update a task. Returns None if not found."""

    def update_status(self, task_id: int, status: TaskStatus) -> Task | None:
        """Update task status. Returns None if not found."""

    def delete_task(self, task_id: int) -> bool:
        """Delete by id. Returns True if a row was removed."""

    def clear(self) -> None:
        """Wipe all data (tests only)."""


# ---------------------------------------------------------------------------
# In-memory implementation
# ---------------------------------------------------------------------------

class InMemoryTaskStore:
    """Thread-safe in-memory store for local development and tests."""

    backend = "in_memory"

    def __init__(self) -> None:
        self._lock = Lock()
        self._next_id = 1
        self._tasks: dict[int, Task] = {}

    def list_tasks(
        self,
        *,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> tuple[list[Task], int]:
        with self._lock:
            tasks = [self._tasks[i] for i in sorted(self._tasks)]
            if status is not None:
                tasks = [t for t in tasks if t.status == status]
            if priority is not None:
                tasks = [t for t in tasks if t.priority == priority]
            total = len(tasks)
            return tasks[skip : skip + limit], total

    def get_task(self, task_id: int) -> Task | None:
        with self._lock:
            return self._tasks.get(task_id)

    def create_task(self, payload: TaskCreate) -> Task:
        with self._lock:
            now = datetime.now(timezone.utc)
            task = Task(
                id=self._next_id,
                title=payload.title.strip(),
                description=payload.description.strip(),
                status=TaskStatus.TODO,
                priority=payload.priority,
                created_at=now,
                updated_at=now,
            )
            self._tasks[self._next_id] = task
            self._next_id += 1
            return task

    def update_task(self, task_id: int, payload: TaskUpdate) -> Task | None:
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                return None
            updates: dict[str, Any] = {"updated_at": datetime.now(timezone.utc)}
            if payload.title is not None:
                updates["title"] = payload.title.strip()
            if payload.description is not None:
                updates["description"] = payload.description.strip()
            if payload.priority is not None:
                updates["priority"] = payload.priority
            updated = task.model_copy(update=updates)
            self._tasks[task_id] = updated
            return updated

    def update_status(self, task_id: int, status: TaskStatus) -> Task | None:
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                return None
            updated = task.model_copy(
                update={"status": status, "updated_at": datetime.now(timezone.utc)}
            )
            self._tasks[task_id] = updated
            return updated

    def delete_task(self, task_id: int) -> bool:
        with self._lock:
            return self._tasks.pop(task_id, None) is not None

    def clear(self) -> None:
        with self._lock:
            self._tasks.clear()
            self._next_id = 1


# ---------------------------------------------------------------------------
# Supabase implementation
# ---------------------------------------------------------------------------

class SupabaseTaskStore:
    """Supabase-backed (PostgreSQL) task storage."""

    backend = "supabase"

    def __init__(self, table_name: str) -> None:
        self._table = table_name

    def _client(self):  # type: ignore[return]
        return get_client()

    def list_tasks(
        self,
        *,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        skip: int = 0,
        limit: int = 50,
    ) -> tuple[list[Task], int]:
        # Count query
        count_query = self._client().table(self._table).select("id", count="exact")
        if status is not None:
            count_query = count_query.eq("status", status.value)
        if priority is not None:
            count_query = count_query.eq("priority", priority.value)
        count_resp = count_query.execute()
        total = count_resp.count or 0

        # Data query with pagination
        query = (
            self._client()
            .table(self._table)
            .select("*")
            .order("id", desc=False)
            .range(skip, skip + limit - 1)
        )
        if status is not None:
            query = query.eq("status", status.value)
        if priority is not None:
            query = query.eq("priority", priority.value)
        response = query.execute()
        rows = response.data or []
        return [Task.model_validate(row) for row in rows], total

    def get_task(self, task_id: int) -> Task | None:
        response = self._client().table(self._table).select("*").eq("id", task_id).execute()
        rows = response.data or []
        return Task.model_validate(rows[0]) if rows else None

    def create_task(self, payload: TaskCreate) -> Task:
        response = (
            self._client()
            .table(self._table)
            .insert(
                {
                    "title": payload.title.strip(),
                    "description": payload.description.strip(),
                    "status": TaskStatus.TODO.value,
                    "priority": payload.priority.value,
                }
            )
            .execute()
        )
        rows = response.data or []
        if not rows:
            raise RuntimeError("Supabase insert did not return a task row.")
        return Task.model_validate(rows[0])

    def update_task(self, task_id: int, payload: TaskUpdate) -> Task | None:
        if not self.get_task(task_id):
            return None
        updates: dict[str, Any] = {}
        if payload.title is not None:
            updates["title"] = payload.title.strip()
        if payload.description is not None:
            updates["description"] = payload.description.strip()
        if payload.priority is not None:
            updates["priority"] = payload.priority.value
        if updates:
            self._client().table(self._table).update(updates).eq("id", task_id).execute()
        return self.get_task(task_id)

    def update_status(self, task_id: int, status: TaskStatus) -> Task | None:
        if not self.get_task(task_id):
            return None
        self._client().table(self._table).update({"status": status.value}).eq(
            "id", task_id
        ).execute()
        return self.get_task(task_id)

    def delete_task(self, task_id: int) -> bool:
        if not self.get_task(task_id):
            return False
        self._client().table(self._table).delete().eq("id", task_id).execute()
        return True

    def clear(self) -> None:
        self._client().table(self._table).delete().gt("id", 0).execute()


# ---------------------------------------------------------------------------
# Factory
# ---------------------------------------------------------------------------

def _build_task_store() -> TaskStoreProtocol:
    """Select and initialise the correct persistence backend."""
    if config.TASK_TRACKER_STORAGE == "in_memory":
        logger.info("Task store → in_memory")
        return InMemoryTaskStore()

    client = get_client()
    if client is None:
        logger.warning("Supabase unavailable — falling back to in_memory store.")
        return InMemoryTaskStore()

    logger.info("Task store → supabase (table: %s)", config.SUPABASE_TASKS_TABLE)
    return SupabaseTaskStore(table_name=config.SUPABASE_TASKS_TABLE)


task_store: TaskStoreProtocol = _build_task_store()
