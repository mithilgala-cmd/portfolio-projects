# Task Tracker API

A FastAPI task management API that uses Supabase as the database backend (with local in-memory fallback for development/tests).

## Features

- Supabase-backed task persistence
- Task CRUD with status workflow (`todo`, `in_progress`, `done`)
- Environment-driven storage mode (`supabase` or `in_memory`)
- Health endpoint with backend metadata
- Unit tests for endpoint behavior

## Tech Stack

- Python
- FastAPI
- Supabase (Postgres)
- Pydantic
- pytest

## Project Layout

```text
task_tracker_api/
|-- src/
|   |-- main.py
|   |-- config.py
|   |-- models.py
|   |-- store.py
|   `-- routers/
|-- supabase/
|   `-- schema.sql
|-- tests/
|-- .env.example
`-- requirements.txt
```

## Supabase Setup

1. Create a Supabase project.
2. Run [`supabase/schema.sql`](supabase/schema.sql) in SQL Editor.
3. Copy `.env.example` to `.env` and set:
   - `SUPABASE_URL`
   - `SUPABASE_SERVICE_ROLE_KEY`

Use service role key only in backend environments.

## Run Locally

```bash
cd backend/projects/task_tracker_api
pip install -r requirements.txt
copy .env.example .env
uvicorn src.main:app --reload --port 8002
```

Docs: `http://127.0.0.1:8002/docs`

## Test

```bash
pytest tests -v
```

Tests force `in_memory` mode automatically so they run without external services.

## Main Endpoints

- `GET /health`
- `GET /tasks`
- `POST /tasks`
- `PATCH /tasks/{task_id}/status`
- `DELETE /tasks/{task_id}`
