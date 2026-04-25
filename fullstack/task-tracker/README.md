# Task Tracker Pro

<div align="center">

![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-8-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-22%20passing-brightgreen?style=for-the-badge&logo=pytest&logoColor=white)

**A production-ready, full-stack Kanban task management system.**  
FastAPI backend · React frontend · Supabase (PostgreSQL) · Clean layered architecture

</div>

---

## 📌 Overview

Task Tracker Pro is a complete full-stack application built to demonstrate production-level engineering practices. It features a FastAPI REST API with a clean layered architecture (routers → services → store → DB), a React Kanban board with real-time UI updates, and Supabase as the cloud database with an in-memory fallback for local development.

---

## ✨ Features

### Backend
- ✅ RESTful API with 7 endpoints (full CRUD)
- ✅ Clean layered architecture — `routers → services → store → db`
- ✅ Priority levels — `low` · `medium` · `high`
- ✅ Status workflow — `todo → in_progress → done`
- ✅ Combinable filters — `?status=` · `?priority=`
- ✅ Server-side pagination — `?page=` · `?size=`
- ✅ Dual persistence — Supabase in production, in-memory fallback for dev
- ✅ Auto-managed timestamps via DB trigger
- ✅ 22 unit tests (all passing)

### Frontend
- ✅ 3-column Kanban board — Planned · In Motion · Delivered
- ✅ Create tasks with title, description & priority
- ✅ Edit tasks via polished inline modal
- ✅ Priority badges (color-coded per card)
- ✅ Live search — filter by title or description
- ✅ Status + Priority tab filters
- ✅ Live stats — total, in-motion, completion % with animated progress bar
- ✅ Auto-dismissing success/error banners
- ✅ Fully responsive (mobile → desktop)

---

## 🏗️ Project Structure

```text
task-tracker/
├── backend/                    # FastAPI application
│   ├── src/
│   │   ├── db/
│   │   │   └── client.py       # Supabase client singleton
│   │   ├── services/
│   │   │   └── task_service.py # Business logic layer
│   │   ├── routers/
│   │   │   ├── tasks.py        # Task HTTP endpoints (thin layer)
│   │   │   └── health.py       # Health check endpoint
│   │   ├── main.py             # App entry point + CORS
│   │   ├── config.py           # Env-driven configuration
│   │   ├── models.py           # Pydantic schemas
│   │   └── store.py            # InMemory + Supabase stores
│   ├── supabase/
│   │   └── schema.sql          # DB schema + migration snippet
│   ├── tests/                  # 22 pytest tests
│   ├── .env.example
│   ├── requirements.txt
│   └── README.md               # Backend-specific docs
│
└── frontend/                   # React + Vite application
    ├── src/
    │   ├── components/
    │   │   ├── TaskColumn.jsx       # Board column with cards
    │   │   ├── TaskComposer.jsx     # New task form
    │   │   └── EditTaskModal.jsx    # Inline edit modal
    │   ├── services/
    │   │   └── tasks.js            # Axios API client
    │   ├── App.jsx                 # Root component + state
    │   ├── main.jsx
    │   └── index.css              # Design system + styles
    ├── .env.example
    ├── package.json
    └── README.md                  # Frontend-specific docs
```

---

## 🧱 Architecture

```
HTTP Request
     │
     ▼
┌─────────────┐
│   Router    │  ← parses HTTP, validates shape, returns response
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Service   │  ← business logic, pagination, logging, 404 raises
└──────┬──────┘
       │
       ▼
┌─────────────┐
│    Store    │  ← persistence abstraction (in-memory or Supabase)
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  DB Client  │  ← Supabase singleton (src/db/client.py)
└─────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 20+

### 1 — Clone

```bash
git clone https://github.com/mithilgala-cmd/portfolio-projects.git
cd portfolio-projects/fullstack/task-tracker
```

### 2 — Start the Backend

```bash
cd backend
pip install -r requirements.txt
cp .env.example .env          # fill in Supabase credentials (optional)
uvicorn src.main:app --reload --port 8002
```

> **No Supabase?** Leave credentials empty — the API automatically falls back to in-memory storage.

API docs: `http://127.0.0.1:8002/docs`

### 3 — Start the Frontend

```bash
cd ../frontend
npm install
cp .env.example .env          # set VITE_TASK_API_BASE_URL if needed
npm run dev
```

App: `http://localhost:5173`

### 4 — Run Backend Tests

```bash
cd backend
python -m pytest tests -v
```

---

## 🌐 API Summary

| Method   | Endpoint                   | Description                          |
|----------|----------------------------|--------------------------------------|
| `GET`    | `/health`                  | Service health check                 |
| `GET`    | `/tasks`                   | List tasks (filters + pagination)    |
| `GET`    | `/tasks/{id}`              | Get a single task                    |
| `POST`   | `/tasks`                   | Create a task                        |
| `PATCH`  | `/tasks/{id}`              | Update title / description / priority|
| `PATCH`  | `/tasks/{id}/status`       | Update task status                   |
| `DELETE` | `/tasks/{id}`              | Delete a task                        |

**Filter & paginate:**
```
GET /tasks?status=todo&priority=high&page=1&size=10
```

---

## 🔗 More Details

| Document | Description |
|---|---|
| [Backend README](./backend/README.md) | API docs, endpoints, architecture, curl examples, test guide |
| [Frontend README](./frontend/README.md) | Setup, features, env vars, build instructions |

---

## 🛠️ Tech Stack

| Layer      | Technology                        |
|------------|-----------------------------------|
| Backend    | Python 3.11+, FastAPI 0.115       |
| Database   | Supabase (PostgreSQL)             |
| Validation | Pydantic v2                       |
| Testing    | pytest, httpx                     |
| Frontend   | React 19, Vite 8                  |
| HTTP       | Axios                             |
| Icons      | Lucide React                      |
| Fonts      | Google Fonts (Manrope, Sora)      |
| Styling    | Vanilla CSS                       |
