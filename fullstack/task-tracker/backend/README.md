# Task Tracker API

A production-style FastAPI REST API for task management with Supabase persistence and an in-memory fallback for local development and testing.

## Features

- ✅ Full CRUD — create, read, update, delete tasks
- ✅ Priority levels — `low`, `medium`, `high` per task
- ✅ Status workflow — `todo → in_progress → done`
- ✅ Status filter — `GET /tasks?status=todo`
- ✅ Dual persistence — Supabase (Postgres) in production, in-memory for dev/tests
- ✅ Auto-timestamp — `updated_at` managed by a DB trigger
- ✅ 20+ unit tests with `pytest`

## Tech Stack

| Layer       | Technology              |
|-------------|-------------------------|
| Framework   | FastAPI                 |
| Database    | Supabase (PostgreSQL)   |
| Validation  | Pydantic v2             |
| Testing     | pytest + httpx          |
| Config      | python-dotenv           |

## Project Layout

```text
backend/
├── src/
│   ├── main.py        # App entry point, CORS, router wiring
│   ├── config.py      # Env-driven configuration
│   ├── models.py      # Pydantic models (Task, TaskCreate, TaskUpdate)
│   ├── store.py       # InMemoryTaskStore + SupabaseTaskStore
│   └── routers/
│       ├── tasks.py   # Task CRUD endpoints
│       └── health.py  # Health check
├── supabase/
│   └── schema.sql     # DB schema + migration snippet
├── tests/
│   ├── conftest.py
│   ├── test_tasks.py  # 20 endpoint tests
│   └── test_health.py
├── .env.example
└── requirements.txt
```

## API Endpoints

| Method   | Path                       | Description                        |
|----------|----------------------------|------------------------------------|
| `GET`    | `/health`                  | Service health + backend info      |
| `GET`    | `/tasks`                   | List all tasks (optional `?status=`)|
| `GET`    | `/tasks/{id}`              | Get a single task                  |
| `POST`   | `/tasks`                   | Create a task                      |
| `PATCH`  | `/tasks/{id}`              | Update title / description / priority |
| `PATCH`  | `/tasks/{id}/status`       | Update task status                 |
| `DELETE` | `/tasks/{id}`              | Delete a task                      |

## Supabase Setup

1. Create a Supabase project at [supabase.com](https://supabase.com).
2. Run [`supabase/schema.sql`](supabase/schema.sql) in the SQL Editor.
3. Copy `.env.example` → `.env` and fill in your credentials:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

> **Note:** If no credentials are provided the API automatically falls back to in-memory storage.

## Run Locally

```bash
cd fullstack/task-tracker/backend
pip install -r requirements.txt
cp .env.example .env   # fill in your Supabase credentials
uvicorn src.main:app --reload --port 8002
```

Interactive docs: `http://127.0.0.1:8002/docs`

## Run Tests

```bash
pytest tests -v
```

Tests always use the in-memory store (set by `conftest.py`) — no external services needed.
