# Code Review AI — Backend

A FastAPI backend that uses **Google Gemini** to perform AI-powered code reviews. Accepts a code snippet and language, then returns a structured review with a quality score, complexity rating, issues by severity, improvement suggestions, and positive feedback.

---

## Features

- 🤖 **AI-powered review** via Google Gemini (`gemini-2.5-flash`)
- 📊 **Overall quality score** (0–100) and complexity rating
- 🔴 **Issues by severity** — errors, warnings, and info-level notes
- 💡 **Improvement suggestions** and positive feedback
- 🌐 **15+ languages** supported (Python, JS, TS, Java, C++, Go, Rust, and more)
- ⚡ **CORS-enabled** — ready to pair with the React frontend at `localhost:5173`
- 📄 **Auto-generated Swagger UI** at `/docs`

---

## Project Structure

```
code_review_ai/
├── main.py             # FastAPI app, CORS, /review endpoint
├── .env                # API key (not tracked)
├── .env.example        # Template for environment variables
└── requirements.txt
```

---

## Quick Start

### 1. Install dependencies

```bash
cd backend/projects/code_review_ai
pip install -r requirements.txt
```

### 2. Configure environment

```bash
copy .env.example .env
# Open .env and set: GEMINI_API_KEY=your_key_here
```

Get a free API key from [Google AI Studio](https://aistudio.google.com/app/apikey).

### 3. Run the server

```bash
uvicorn main:app --reload --port 8001
```

The API will be available at `http://localhost:8001`.
Interactive docs at `http://localhost:8001/docs`.

---

## API

### `POST /review`

**Request body:**
```json
{
  "code": "def add(a, b):\n    return a + b",
  "language": "python"
}
```

**Response:**
```json
{
  "summary": "Clean and simple function with no issues.",
  "overall_score": 92,
  "complexity": "Low",
  "issues": [],
  "improvements": ["Add type hints for better readability"],
  "positive_points": ["Correct logic", "Clear naming"]
}
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GEMINI_API_KEY` | Your Google Gemini API key |

---

## Supported Languages

Python, JavaScript, TypeScript, Java, C++, Go, Rust, C#, Ruby, PHP, Swift, Kotlin, and more.

---

## Stack

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-4285F4?style=flat&logo=google&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063?style=flat&logo=pydantic&logoColor=white)

---

> **Frontend:** The React frontend lives at `frontend/code-review-ai/`. Run both the backend (port 8001) and frontend (port 5173) together for the full experience.
