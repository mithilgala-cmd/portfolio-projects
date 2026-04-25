"""Task storage implementations."""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from threading import Lock
from typing import Any, Protocol

from src import config
from src.models import Task, TaskCreate, TaskStatus

try:
    from supabase import Client, create_client
except ImportError:  # pragma: no cover - exercised when dependency is missing locally
    Client = Any  # type: ignore[assignment]
    create_client = None

logger = logging.getLogger(__name__)


class TaskStoreProtocol(Protocol):
    """Contract for task persistence layers."""

    backend: str

    def list_tasks(self) -> list[Task]:
        """Return all tasks in stable order."""

    def create_task(self, payload: TaskCreate) -> Task:
        """Create a task and return the stored object."""

    def update_status(self, task_id: int, status: TaskStatus) -> Task | None:
        """Update task status or return None if missing."""

    def delete_task(self, task_id: int) -> bool:
        """Delete by id and report whether a row existed."""

    def clear(self) -> None:
        """Reset backing store for tests."""


class InMemoryTaskStore:
    """Thread-safe in-memory store for local/test fallback."""

    backend = "in_memory"

    def __init__(self) -> None:
        self._lock = Lock()
        self._next_id = 1
        self._tasks: dict[int, Task] = {}

    def list_tasks(self) -> list[Task]:
        with self._lock:
            return [self._tasks[task_id] for task_id in sorted(self._tasks)]

    def create_task(self, payload: TaskCreate) -> Task:
        with self._lock:
            now = datetime.now(timezone.utc)
            task = Task(
                id=self._next_id,
                title=payload.title.strip(),
                description=payload.description.strip(),
                status=TaskStatus.TODO,
                created_at=now,
                updated_at=now,
            )
            self._tasks[self._next_id] = task
            self._next_id += 1
            return task

    def update_status(self, task_id: int, status: TaskStatus) -> Task | None:
        with self._lock:
            task = self._tasks.get(task_id)
            if task is None:
                return None

            updated_task = task.model_copy(
                update={"status": status, "updated_at": datetime.now(timezone.utc)}
            )
            self._tasks[task_id] = updated_task
            return updated_task

    def delete_task(self, task_id: int) -> bool:
        with self._lock:
            return self._tasks.pop(task_id, None) is not None

    def clear(self) -> None:
        with self._lock:
            self._tasks.clear()
            self._next_id = 1


class SupabaseTaskStore:
    """Supabase-backed task storage."""

    backend = "supabase"

    def __init__(self, client: Client, table_name: str) -> None:
        self._client = client
        self._table_name = table_name

    def list_tasks(self) -> list[Task]:
        response = (
            self._client.table(self._table_name).select("*").order("id", desc=False).execute()
        )
        rows = response.data or []
        return [Task.model_validate(row) for row in rows]

    def create_task(self, payload: TaskCreate) -> Task:
        response = (
            self._client.table(self._table_name)
            .insert(
                {
                    "title": payload.title.strip(),
                    "description": payload.description.strip(),
                    "status": TaskStatus.TODO.value,
                }
            )
            .execute()
        )
        rows = response.data or []
        if not rows:
            raise RuntimeError("Supabase insert did not return a task row.")
        return Task.model_validate(rows[0])

    def update_status(self, task_id: int, status: TaskStatus) -> Task | None:
        existing = self._client.table(self._table_name).select("id").eq("id", task_id).execute()
        if not existing.data:
            return None

        self._client.table(self._table_name).update({"status": status.value}).eq(
            "id", task_id
        ).execute()
        refreshed = self._client.table(self._table_name).select("*").eq("id", task_id).execute()
        rows = refreshed.data or []
        if not rows:
            return None
        return Task.model_validate(rows[0])

    def delete_task(self, task_id: int) -> bool:
        existing = self._client.table(self._table_name).select("id").eq("id", task_id).execute()
        if not existing.data:
            return False
        self._client.table(self._table_name).delete().eq("id", task_id).execute()
        return True

    def clear(self) -> None:
        self._client.table(self._table_name).delete().gt("id", 0).execute()


def _build_task_store() -> TaskStoreProtocol:
    """Create the configured persistence implementation."""
    if config.TASK_TRACKER_STORAGE == "in_memory":
        logger.info("Task store configured: in_memory")
        return InMemoryTaskStore()

    if create_client is None:
        logger.warning(
            "supabase dependency is not installed. Falling back to in_memory store."
        )
        return InMemoryTaskStore()

    if not config.SUPABASE_URL or not config.SUPABASE_KEY:
        logger.warning(
            "Supabase credentials are missing. Falling back to in_memory store."
        )
        return InMemoryTaskStore()

    try:
        client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
        logger.info("Task store configured: supabase (%s)", config.SUPABASE_TASKS_TABLE)
        return SupabaseTaskStore(client=client, table_name=config.SUPABASE_TASKS_TABLE)
    except Exception as exc:  # pragma: no cover - runtime guard
        logger.exception("Failed to initialize Supabase store: %s", exc)
        return InMemoryTaskStore()


task_store: TaskStoreProtocol = _build_task_store()
