# Portfolio Projects

<div align="center">

![GitHub last commit](https://img.shields.io/github/last-commit/mithilgala-cmd/portfolio-projects?style=for-the-badge&logo=github)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=for-the-badge&logo=fastapi&logoColor=white)

A curated portfolio of full-stack, backend, machine learning, cybersecurity,  
and DSA projects — built for software engineering placements.

</div>

---

## Repository Structure

```text
portfolio-projects/
├── fullstack/
│   ├── task-tracker/           Featured — Full-stack Kanban app
│   │   ├── backend/            FastAPI + Supabase REST API
│   │   └── frontend/           React + Vite Kanban board
│   ├── code-review-ai/
│   │   ├── backend/            FastAPI + Google Gemini LLM
│   │   └── frontend/           Monaco editor + AI review UI
│   ├── news-aggregator/
│   │   ├── backend/            FastAPI async news API
│   │   └── frontend/           React news search UI
│   ├── bento-dashboard/        React stats + chart dashboard
│   └── crypto-trading-dashboard/ Featured — Real-time trading app
│       ├── backend/            FastAPI + Binance WebSockets
│       └── frontend/           Next.js + Lightweight Charts
├── Cybersecurity/              End-to-end encrypted chat app
├── machine_learning/           House price prediction & CNN classifier
└── dsa-python/                 Pattern-wise DSA practice + tests
```

---

## Project Index

| Area | Project | What it demonstrates | Stack |
|---|---|---|---|
| Full-Stack | [`task-tracker`](fullstack/task-tracker/) | Clean arch · CRUD API · React Kanban · Supabase · 22 tests | FastAPI · React · Supabase |
| Full-Stack | [`code-review-ai`](fullstack/code-review-ai/) | LLM API integration · Monaco editor UI | FastAPI · Gemini · React |
| Full-Stack | [`news-aggregator`](fullstack/news-aggregator/) | Async API calls · caching · search UI | FastAPI · httpx · React |
| Full-Stack | [`crypto-trading-dashboard`](fullstack/crypto-trading-dashboard/) | WebSockets · Real-time charts · Bot logic · Premium UI | FastAPI · Next.js · Redis |
| Frontend | [`bento-dashboard`](fullstack/bento-dashboard/) | Stateful dashboard · charts · local persistence | React · Vite · Recharts |
| Cybersecurity | [`Cybersecurity`](Cybersecurity/) | E2E encryption · auth · rate limiting · relay model | Python · Flask · PyCryptodome |
| Machine Learning | [`house_price_prediction`](machine_learning/projects/house_price_prediction/) | Tabular ML pipeline · preprocessing · inference | scikit-learn · pandas |
| Machine Learning | [`cnn_image_classifier`](machine_learning/projects/cnn_image_classifier/) | CNN architecture · data augmentation · evaluation | TensorFlow · Keras |
| Interview Prep | [`dsa-python`](dsa-python/) | Pattern-wise DSA · roadmap · pytest suite | Python · pytest |

---

## Featured Project — Task Tracker Pro

> A production-ready full-stack task management system built to demonstrate real engineering depth.

**Backend highlights:**
- Clean layered architecture: `routers → services → store → db`
- 7 REST endpoints with pagination and dual filters (`?status=` + `?priority=`)
- Supabase (PostgreSQL) with in-memory fallback for dev
- 22 passing unit tests — no external services needed

**Frontend highlights:**
- 3-column Kanban board (Planned · In Motion · Delivered)
- Inline task editing via accessible modal
- Live search + status & priority tab filters
- Animated stats header with completion progress bar

[View Task Tracker README](fullstack/task-tracker/README.md)

---

## Quick Start — Task Tracker

```bash
git clone https://github.com/mithilgala-cmd/portfolio-projects.git
cd portfolio-projects/fullstack/task-tracker

# Backend
cd backend
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8002

# Frontend (in a new terminal)
cd ../frontend
npm install && npm run dev
```

API docs: `http://127.0.0.1:8002/docs` · App: `http://localhost:5173`

---

## Other Quick Starts

**News Aggregator:**
```bash
cd fullstack/news-aggregator/backend && pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000

cd ../frontend && npm install && npm run dev
```

**Code Review AI:**
```bash
cd fullstack/code-review-ai/backend && pip install -r requirements.txt
uvicorn main:app --reload --port 8001

cd ../frontend && npm install && npm run dev
```

**Crypto Trading Dashboard:**
```bash
cd fullstack/crypto-trading-dashboard/backend && pip install -r requirements.txt
uvicorn main:app --reload --port 8001

cd ../frontend && npm install && npm run dev
```

**Cybersecurity Chat:**
```bash
cd Cybersecurity && pip install -r requirements.txt
python server/server.py   # terminal 1
python client/client.py   # terminal 2
```

**DSA Test Suite:**
```bash
cd dsa-python && pip install -r requirements.txt && python -m pytest
```

---

## Placement Highlights

- **Full-stack depth** — FastAPI + Next.js/React across multiple projects with real API design patterns
- **Real-time systems** — WebSocket streaming for live market data (Binance API integration)
- **Clean architecture** — service layer separation, dependency inversion, protocol-based store abstraction
- **Database experience** — Supabase (PostgreSQL), schema design, triggers, migrations
- **Test culture** — pytest with in-memory fixtures; no flaky external dependencies
- **Security** — password hashing, account lockout, E2E encryption, rate limiting
- **Machine Learning** — deep learning with CNNs (TensorFlow/Keras), tabular pipelines (scikit-learn), augmentation, and model evaluation
- **Code quality** — type hints throughout Python, Pydantic validation, ESLint

---

## Prerequisites

| Requirement | Version |
|---|---|
| Python | 3.11+ |
| Node.js | 20+ |
| Git | latest |

---

## Notes

- API keys are required for external-provider projects (NewsAPI, Google Gemini, Supabase).
- Each project folder contains its own README with detailed setup instructions.
- Large generated artifacts (`node_modules`, `dist`, `__pycache__`) are excluded via `.gitignore`.
- This repo is continuously improved — see commit history for recent changes.
