# Task Tracker Pro — Frontend

<div align="center">

![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-8-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Axios](https://img.shields.io/badge/Axios-1.x-5A29E4?style=for-the-badge&logo=axios&logoColor=white)
![Lucide](https://img.shields.io/badge/Lucide_React-Icons-F56565?style=for-the-badge)
![CSS](https://img.shields.io/badge/Vanilla_CSS-Design_System-1572B6?style=for-the-badge&logo=css3&logoColor=white)

A premium-feel React Kanban board that connects to the Task Tracker API.  
Create · edit · filter · delete tasks — all with smooth animations and a polished UI.

</div>

---

## Features

| Feature | Details |
|---|---|
| **Kanban Board** | 3 columns — Planned · In Motion · Delivered |
| **Create Tasks** | Title, description, and priority selector in one form |
| **Edit Tasks** | Inline modal — update title, description, or priority |
| **Priority Badges** | Color-coded pills per card (🔴 High · 🟡 Medium · 🟢 Low) |
| **Status Actions** | One-click status change directly on each card |
| **Delete** | Instant remove with optimistic UI update |
| **Live Search** | Real-time filter by title or description |
| **Status Filter** | Tab filter: All · To Do · In Progress · Done |
| **Priority Filter** | Tab filter: All · High · Medium · Low |
| **Stats Header** | Total tasks · In-motion count · Completion % with progress bar |
| **Auto-dismiss Banners** | Success/error messages clear after 3 seconds |
| **Responsive** | Fully adaptive from mobile to wide desktop |

---

## Project Structure

```text
src/
├── components/
│   ├── TaskColumn.jsx     # Board column: renders cards, priority badges, timestamps
│   ├── TaskComposer.jsx   # New task form (title · description · priority)
│   └── EditTaskModal.jsx  # Accessible edit modal (Escape key · backdrop close)
├── services/
│   └── tasks.js           # Axios API client (CRUD + filter + pagination)
├── App.jsx                # Root component — state, handlers, layout
├── main.jsx               # React entry point
└── index.css              # Full design system (tokens, components, animations)
```

---

## Component Overview

### `TaskComposer`
Form to create a new task. Fields: **title** (required), **description** (optional), **priority** (dropdown). Clears on successful submit.

### `TaskColumn`
Renders a filtered list of task cards for a given status. Each card shows:
- Task title and description
- Priority badge (color-coded)
- Creation date
- Status change buttons
- Edit (✏️) and Delete (🗑️) icon buttons

### `EditTaskModal`
Accessible modal dialog for editing a task:
- Prefilled with current title, description, and priority
- Priority selector with color-coded option buttons
- Closes on **Save**, **Cancel**, **Escape key**, or **backdrop click**
- Keyboard focus managed on open

### `tasks.js` (Service)
All API calls via Axios. Functions exported:

| Function | Description |
|---|---|
| `fetchTasks({ status, priority, page, size })` | List tasks with optional filters |
| `getTask(taskId)` | Fetch a single task |
| `createTask(payload)` | Create a new task |
| `updateTask(taskId, payload)` | Update title / description / priority |
| `updateTaskStatus(taskId, status)` | Change task status |
| `deleteTask(taskId)` | Delete a task |

---

## Tech Stack

| Layer     | Technology                      |
|-----------|---------------------------------|
| Framework | React 19 + Vite 8               |
| HTTP      | Axios 1.x                       |
| Icons     | Lucide React                    |
| Fonts     | Google Fonts — Manrope · Sora   |
| Styling   | Vanilla CSS (custom design system) |

---

## Setup

```bash
cd fullstack/task-tracker/frontend
npm install
cp .env.example .env
npm run dev
```

The app connects to `http://localhost:8002` by default.  
Make sure the backend is running first.

---

## Environment Variables

| Variable                 | Default                 | Description                |
|--------------------------|-------------------------|----------------------------|
| `VITE_TASK_API_BASE_URL` | `http://localhost:8002` | Task Tracker API base URL  |

---

## Available Scripts

| Script          | Description                        |
|-----------------|------------------------------------|
| `npm run dev`   | Start the Vite dev server          |
| `npm run build` | Build for production (`dist/`)     |
| `npm run lint`  | Run ESLint                         |
| `npm run preview` | Preview the production build     |

---

## Design System

All styling lives in `src/index.css` using CSS custom properties (design tokens):

```css
--bg            /* page background    */
--ink           /* primary text       */
--muted         /* secondary text     */
--panel         /* glass card surface */
--accent        /* brand orange       */
--good          /* success green      */
--danger        /* error red          */
--warn          /* warning amber      */
```

Animations: `rise` (cards on mount) · `fade-in` (modal overlay) · `slide-up` (modal card) · `spin` (loading spinner)
