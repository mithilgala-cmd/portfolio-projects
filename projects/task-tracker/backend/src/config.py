"""Application configuration."""

import os

from dotenv import load_dotenv

load_dotenv()

APP_NAME = "Task Tracker API"
APP_VERSION = "1.1.0"
APP_DESCRIPTION = "A FastAPI service to track tasks with Supabase persistence."

SERVER_HOST = os.getenv("TASK_TRACKER_HOST", "127.0.0.1")
SERVER_PORT = int(os.getenv("TASK_TRACKER_PORT", "8002"))

TASK_TRACKER_STORAGE = os.getenv("TASK_TRACKER_STORAGE", "supabase").strip().lower()

SUPABASE_URL = os.getenv("SUPABASE_URL", "").strip()
SUPABASE_KEY = (
    os.getenv("SUPABASE_SERVICE_ROLE_KEY")
    or os.getenv("SUPABASE_SERVICE_KEY")
    or os.getenv("SUPABASE_KEY", "")
).strip()
SUPABASE_TASKS_TABLE = os.getenv("SUPABASE_TASKS_TABLE", "tasks").strip() or "tasks"

FRONTEND_ORIGIN = os.getenv("FRONTEND_ORIGIN", "*").strip()


def supabase_is_configured() -> bool:
    """Check whether Supabase connection settings are present."""
    return bool(SUPABASE_URL and SUPABASE_KEY)
