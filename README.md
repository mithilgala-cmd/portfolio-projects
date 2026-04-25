# Portfolio Projects

A curated portfolio of backend, frontend, machine learning, cybersecurity, and DSA work for software engineering placements.

## Project Index

| Area | Project | What it demonstrates | Main stack |
|---|---|---|---|
| Cybersecurity | [`Cybersecurity`](Cybersecurity/) | End-to-end encrypted chat, authentication, rate limiting, secure relay model | Python, sockets, Flask, SQLite, PyCryptodome |
| Backend API | [`fullstack/news-aggregator/backend`](fullstack/news-aggregator/backend/) | Async API integration, caching, schema validation, tests | FastAPI, httpx, Pydantic |
| Backend API + AI | [`fullstack/code-review-ai/backend`](fullstack/code-review-ai/backend/) | LLM-integrated API design and structured response handling | FastAPI, Google Gemini |
| Backend API | [`fullstack/task-tracker/backend`](fullstack/task-tracker/backend/) | Supabase-backed CRUD API with status workflow and tests | FastAPI, Supabase, Pydantic |
| Frontend | [`fullstack/news-aggregator/frontend`](fullstack/news-aggregator/frontend/) | API-driven React UI with search and loading/error states | React, Vite |
| Frontend | [`fullstack/code-review-ai/frontend`](fullstack/code-review-ai/frontend/) | Monaco-powered code editor UI with AI review workflow | React, Vite, Monaco |
| Frontend | [`fullstack/bento-dashboard`](fullstack/bento-dashboard/) | Stateful dashboard UI with charts and local persistence | React, Vite, Recharts |
| Frontend | [`fullstack/task-tracker/frontend`](fullstack/task-tracker/frontend/) | Premium-feel task board UI with live workflow actions | React, Vite, Axios |
| Machine Learning | [`machine_learning/projects/house_price_prediction`](machine_learning/projects/house_price_prediction/) | Tabular ML pipeline, preprocessing, training, inference scripts | Python, scikit-learn, pandas |
| Interview Prep | [`dsa-python`](dsa-python/) | Pattern-wise DSA structure with tests, roadmap, and project scaffolding | Python, pytest |

## Placement-Focused Highlights

- Full-stack experience across Python APIs and modern React frontends.
- Practical security implementation: password hashing, lockout logic, encryption workflows.
- API design with validation, async calls, and caching.
- ML workflow from preprocessing to model artifact generation.
- Test coverage in core Python projects.

## Quick Start

### Prerequisites

- Python 3.11+
- Node.js 20+
- Git

### 1) Clone and open

```bash
git clone https://github.com/mithilgala-cmd/portfolio-projects.git
cd portfolio-projects
```

### 2) Run a backend API example

```bash
cd fullstack/news-aggregator/backend
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```

### 3) Run a frontend example

```bash
cd fullstack/news-aggregator/frontend
npm install
npm run dev
```

### 4) Run cybersecurity chat

```bash
cd Cybersecurity
pip install -r requirements.txt
python server/server.py
```

In a second terminal:

```bash
cd Cybersecurity
python client/client.py
```

### 5) Run DSA test suite

```bash
cd dsa-python
pip install -r requirements.txt
python -m pytest
```

## Repository Structure

```text
portfolio-projects/
├── fullstack/
│   ├── task-tracker/
│   │   ├── frontend/       # React + Vite task board UI
│   │   └── backend/        # FastAPI + Supabase CRUD API
│   ├── code-review-ai/
│   │   ├── frontend/       # Monaco editor + AI review UI
│   │   └── backend/        # FastAPI + Gemini LLM API
│   ├── news-aggregator/
│   │   ├── frontend/       # React news search UI
│   │   └── backend/        # FastAPI async news API
│   └── bento-dashboard/    # React dashboard with charts
├── Cybersecurity/
├── machine_learning/
└── dsa-python/
```

## Notes

- API keys/credentials are required for external-provider projects (NewsAPI, Gemini, and Supabase where applicable).
- Large/generated artifacts are intentionally ignored from version control.
- This repo is continuously improved; each project folder has its own README with details.
