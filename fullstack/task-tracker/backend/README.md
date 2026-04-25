# Task Tracker API

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-22%20passing-brightgreen?style=for-the-badge&logo=pytest&logoColor=white)

A production-style FastAPI REST API with clean layered architecture,  
Supabase persistence, pagination, dual filters, and full test coverage.

</div>

---

## Architecture

```
HTTP Request
     │
     ▼
┌─────────────┐
│  routers/   │  ← HTTP parsing, status codes, response serialisation
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  services/  │  ← business logic, pagination, structured logging
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   store.py  │  ← persistence abstraction (InMemory or Supabase)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   db/       │  ← Supabase client singleton
└─────────────┘
```

**Folder layout:**

```text
src/
├── db/
│   ├── __init__.py
│   └── client.py          # Supabase lazy-singleton factory
├── services/
│   ├── __init__.py
│   └── task_service.py    # Business logic, pagination, logging, 404 raises
├── routers/
│   ├── __init__.py
│   ├── tasks.py           # Task CRUD endpoints (thin HTTP layer)
│   └── health.py          # Health check
├── main.py                # App entry point, CORS, router registration
├── config.py              # Env-driven configuration (python-dotenv)
├── models.py              # Pydantic schemas (request + response)
└── store.py               # InMemoryTaskStore + SupabaseTaskStore
```

---

## Features

- ✅ Full CRUD — Create, Read, Update, Delete
- ✅ Priority levels — `low` · `medium` · `high`
- ✅ Status workflow — `todo → in_progress → done`
- ✅ Dual filters — `?status=` and `?priority=` (combinable)
- ✅ Server-side pagination — `?page=` / `?size=` with `total` + `pages`
- ✅ Dual persistence — Supabase (prod) · in-memory fallback (dev/test)
- ✅ Auto-timestamp — `updated_at` managed by a PostgreSQL trigger
- ✅ Structured logging throughout all layers
- ✅ Interactive API docs at `/docs` and `/redoc`
- ✅ 22 unit tests (zero external dependencies needed)

---

## Tech Stack

| Layer      | Technology              |
|------------|-------------------------|
| Framework  | FastAPI 0.115           |
| Database   | Supabase (PostgreSQL)   |
| Validation | Pydantic v2             |
| Testing    | pytest 8.3 + httpx      |
| Config     | python-dotenv           |
| Server     | Uvicorn                 |

---

## API Endpoints

| Method   | Path                       | Description                              |
|----------|----------------------------|------------------------------------------|
| `GET`    | `/health`                  | Service health + storage backend info    |
| `GET`    | `/tasks`                   | List tasks with filters + pagination     |
| `GET`    | `/tasks/{id}`              | Get a single task by ID                  |
| `POST`   | `/tasks`                   | Create a new task                        |
| `PATCH`  | `/tasks/{id}`              | Update title / description / priority    |
| `PATCH`  | `/tasks/{id}/status`       | Move task through status workflow        |
| `DELETE` | `/tasks/{id}`              | Permanently delete a task                |

### `GET /tasks` — Query Parameters

| Parameter  | Type     | Default | Description                              |
|------------|----------|---------|------------------------------------------|
| `status`   | string   | —       | Filter: `todo` · `in_progress` · `done`  |
| `priority` | string   | —       | Filter: `low` · `medium` · `high`        |
| `page`     | integer  | `1`     | Page number (1-indexed)                  |
| `size`     | integer  | `20`    | Items per page (max `100`)               |

### Response Shape (`GET /tasks`)

```json
{
  "items":  [ { "id": 1, "title": "...", "status": "todo", "priority": "high", ... } ],
  "total":  42,
  "page":   1,
  "size":   20,
  "pages":  3
}
```

---

## Sample API Requests

```bash
# Health check
curl http://localhost:8002/health

# Create a task
curl -X POST http://localhost:8002/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Fix login bug", "description": "OAuth callback 500", "priority": "high"}'

# List all tasks (default page 1, size 20)
curl http://localhost:8002/tasks

# Filter by status + priority + pagination
curl "http://localhost:8002/tasks?status=todo&priority=high&page=1&size=10"

# Get a single task
curl http://localhost:8002/tasks/1

# Update title and priority
curl -X PATCH http://localhost:8002/tasks/1 \
  -H "Content-Type: application/json" \
  -d '{"title": "Fix OAuth callback", "priority": "medium"}'

# Move task to in_progress
curl -X PATCH http://localhost:8002/tasks/1/status \
  -H "Content-Type: application/json" \
  -d '{"status": "in_progress"}'

# Delete a task
curl -X DELETE http://localhost:8002/tasks/1
```

---

## Environment Variables

Copy `.env.example` to `.env` and configure:

```env
# Server
TASK_TRACKER_HOST=127.0.0.1
TASK_TRACKER_PORT=8002
TASK_TRACKER_STORAGE=supabase     # or: in_memory

# CORS — set to your frontend URL in production
FRONTEND_ORIGIN=http://localhost:5173

# Supabase — leave blank to fall back to in-memory store
SUPABASE_URL=https://YOUR_PROJECT_REF.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
SUPABASE_TASKS_TABLE=tasks
```

> ⚠️ Never commit a `.env` file with real credentials.

---

## Supabase Setup

1. Create a project at [supabase.com](https://supabase.com).
2. Open **SQL Editor** and run [`supabase/schema.sql`](supabase/schema.sql).
3. Copy `.env.example` → `.env` and fill in `SUPABASE_URL` and `SUPABASE_SERVICE_ROLE_KEY`.

**Already have the table?** Run only the migration line at the bottom of `schema.sql` to add the `priority` column.

---

## Run Locally

```bash
cd fullstack/task-tracker/backend
pip install -r requirements.txt
cp .env.example .env
uvicorn src.main:app --reload --port 8002
```

- Interactive docs: [http://127.0.0.1:8002/docs](http://127.0.0.1:8002/docs)
- ReDoc: [http://127.0.0.1:8002/redoc](http://127.0.0.1:8002/redoc)

---

## Run Tests

```bash
python -m pytest tests -v
```

All 22 tests run against the **in-memory store** — no Supabase account or `.env` needed.

```
tests/test_health.py   ✅  2 passed
tests/test_tasks.py    ✅ 20 passed
──────────────────────────────────
                       ✅ 22 passed in ~4s
```
