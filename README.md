# Portfolio Projects

A curated portfolio of backend, frontend, machine learning, cybersecurity, and DSA work for software engineering placements.

## Project Index

| Area | Project | What it demonstrates | Main stack |
|---|---|---|---|
| Cybersecurity | [`Cybersecurity`](Cybersecurity/) | End-to-end encrypted chat, authentication, rate limiting, secure relay model | Python, sockets, Flask, SQLite, PyCryptodome |
| Backend API | [`backend/projects/news_aggregator`](backend/projects/news_aggregator/) | Async API integration, caching, schema validation, tests | FastAPI, httpx, Pydantic |
| Backend API + AI | [`backend/projects/code_review_ai`](backend/projects/code_review_ai/) | LLM-integrated API design and structured response handling | FastAPI, Google Gemini |
| Frontend | [`frontend/news-aggregator`](frontend/news-aggregator/) | API-driven React UI with search and loading/error states | React, Vite |
| Frontend | [`frontend/code-review-ai`](frontend/code-review-ai/) | Monaco-powered code editor UI with AI review workflow | React, Vite, Monaco |
| Frontend | [`frontend/bento-dashboard`](frontend/bento-dashboard/) | Stateful dashboard UI with charts and local persistence | React, Vite, Recharts |
| Machine Learning | [`machine_learning/projects/house_price_prediction`](machine_learning/projects/house_price_prediction/) | Tabular ML pipeline, preprocessing, training, inference scripts | Python, scikit-learn, pandas |
| Interview Prep | [`dsa-patterns-python-1`](dsa-patterns-python-1/) | Pattern-wise DSA structure with tests and templates | Python, pytest |

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
cd backend/projects/news_aggregator
pip install -r requirements.txt
uvicorn src.main:app --reload --port 8000
```

### 3) Run a frontend example

```bash
cd frontend/news-aggregator
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

## Repository Structure

```text
portfolio-projects/
|-- Cybersecurity/
|-- backend/
|   `-- projects/
|-- frontend/
|-- machine_learning/
|   `-- projects/
`-- dsa-patterns-python-1/
```

## Notes

- API keys are required for external-provider projects (NewsAPI and Gemini).
- Large/generated artifacts are intentionally ignored from version control.
- This repo is continuously improved; each project folder has its own README with details.
