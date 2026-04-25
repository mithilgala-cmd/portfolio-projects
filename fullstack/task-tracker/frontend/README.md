# Task Tracker Pro Frontend

Premium-style React frontend for `backend/projects/task_tracker_api`.

## Highlights

- Modern 3-column board (`Planned`, `In Motion`, `Delivered`)
- Create, update status, and delete task actions
- Live task stats (total, in progress, completion rate)
- Responsive layout with polished gradients and motion
- API-based architecture with configurable base URL

## Setup

```bash
cd frontend/task-tracker-pro
npm install
copy .env.example .env
npm run dev
```

By default it calls `http://localhost:8002`.

## Environment

- `VITE_TASK_API_BASE_URL` : Task Tracker API base URL

## Build

```bash
npm run build
```
