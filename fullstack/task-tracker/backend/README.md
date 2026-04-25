# Task Tracker API

A production-style FastAPI REST API for task management with Supabase persistence and an in-memory fallback for local development and testing.

## Architecture

```text
src/
├── db/
│   └── client.py          # Supabase client factory (singleton)
├── services/
│   └── task_service.py    # Business logic, pagination, logging
├── routers/
│   ├── tasks.py           # Thin HTTP layer → delegates to service
│   └── health.py          # Health check
├── main.py                # App entry point, CORS, router wiring
├── config.py              # Env-driven configuration
├── models.py              # Pydantic schemas (request + response)
└── store.py               # InMemoryTaskStore + SupabaseTaskStore
```

**Layer responsibilities:**
| Layer | Owns |
|---|---|
| `routers/` | HTTP parsing, status codes, response serialisation |
| `services/` | Business rules, pagination maths, structured logging |
| `store.py` | Persistence (in-memory or Supabase) |
| `db/` | Supabase client lifecycle |

## Features

- ✅ Full CRUD — create, read, update, delete tasks
- ✅ Priority levels — `low`, `medium`, `high`
- ✅ Status workflow — `todo → in_progress → done`
- ✅ Dual filters — `?status=` and `?priority=` (combinable)
- ✅ Pagination — `?page=` / `?size=` with total + page count
- ✅ Dual persistence — Supabase in production, in-memory fallback
- ✅ Auto-timestamp — `updated_at` via DB trigger
- ✅ 22 unit tests (pytest)

## Tech Stack

| Layer     | Technology            |
|-----------|-----------------------|
| Framework | FastAPI               |
| Database  | Supabase (PostgreSQL) |
| Validation| Pydantic v2           |
| Testing   | pytest + httpx        |
| Config    | python-dotenv         |

## API Endpoints

| Method   | Path                       | Description                              |
|----------|----------------------------|------------------------------------------|
| `GET`    | `/health`                  | Service health + backend info            |
| `GET`    | `/tasks`                   | List tasks (filters + pagination)        |
| `GET`    | `/tasks/{id}`              | Get a single task                        |
| `POST`   | `/tasks`                   | Create a task                            |
| `PATCH`  | `/tasks/{id}`              | Update title / description / priority    |
| `PATCH`  | `/tasks/{id}/status`       | Update task status                       |
| `DELETE` | `/tasks/{id}`              | Delete a task                            |

### Query Parameters (GET /tasks)

| Param      | Type     | Default | Description                        |
|------------|----------|---------|------------------------------------|
| `status`   | string   | —       | Filter: `todo`, `in_progress`, `done` |
| `priority` | string   | —       | Filter: `low`, `medium`, `high`    |
| `page`     | integer  | 1       | Page number (1-indexed)            |
| `size`     | integer  | 20      | Items per page (max 100)           |

## Sample API Requests

```bash
# Health check
curl http://localhost:8002/health

# Create a task
curl -X POST http://localhost:8002/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Fix login bug", "description": "OAuth callback 500", "priority": "high"}'

# List all tasks
curl http://localhost:8002/tasks

# Filter by status and priority (paginated)
curl "http://localhost:8002/tasks?status=todo&priority=high&page=1&size=10"

# Get single task
curl http://localhost:8002/tasks/1

# Update task fields
curl -X PATCH http://localhost:8002/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Updated title", "priority": "medium"}'

# Move task to in_progress
curl -X PATCH http://localhost:8002/tasks/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'

# Delete a task
curl -X DELETE http://localhost:8002/tasks/1
```

## Supabase Setup

1. Create a project at [supabase.com](https://supabase.com).
2. Run [`supabase/schema.sql`](supabase/schema.sql) in the SQL Editor.
3. Copy `.env.example` → `.env` and fill in:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

> If no credentials are provided the API automatically falls back to in-memory storage — ideal for local dev without a Supabase account.

## Run Locally

```bash
cd fullstack/task-tracker/backend
pip install -r requirements.txt
cp .env.example .env        # fill in Supabase credentials (optional)
uvicorn src.main:app --reload --port 8002
```

Interactive docs: `http://127.0.0.1:8002/docs`

## Run Tests

```bash
python -m pytest tests -v
```

Tests always use the in-memory store — no external services needed.
