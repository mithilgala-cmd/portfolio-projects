# Task Tracker Pro — Frontend

A premium React frontend for the Task Tracker API. Features a 3-column Kanban board with live task management, priority badges, inline editing, and real-time search filtering.

## Features

- ✅ 3-column Kanban board — Planned / In Motion / Delivered
- ✅ Create tasks with title, description, and priority
- ✅ Edit tasks inline via a polished modal
- ✅ Priority badges — High 🔴 / Medium 🟡 / Low 🟢
- ✅ Search bar — filter by title or description live
- ✅ Status tab filter — view all / todo / in_progress / done
- ✅ One-click status change per card
- ✅ Delete with instant optimistic UI update
- ✅ Live stats — total, in-motion, completion % with progress bar
- ✅ Auto-dismissing success/error banners
- ✅ Fully responsive (mobile → desktop)

## Tech Stack

| Layer     | Technology           |
|-----------|----------------------|
| Framework | React 19 + Vite 8    |
| HTTP      | Axios                |
| Icons     | Lucide React         |
| Fonts     | Google Fonts (Manrope, Sora) |
| Styling   | Vanilla CSS          |

## Setup

```bash
cd fullstack/task-tracker/frontend
npm install
cp .env.example .env   # set VITE_TASK_API_BASE_URL if needed
npm run dev
```

The frontend connects to `http://localhost:8002` by default.

## Environment Variables

| Variable                  | Default                   | Description              |
|---------------------------|---------------------------|--------------------------|
| `VITE_TASK_API_BASE_URL`  | `http://localhost:8002`   | Task Tracker API base URL |

## Build

```bash
npm run build
```
