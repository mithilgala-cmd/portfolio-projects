# Backend

This section covers backend API projects — RESTful services, async APIs, and server-side engineering.

---

## Structure

```
backend/
└── projects/
    ├── news_aggregator/   # FastAPI news aggregation API
    └── code_review_ai/    # FastAPI + Gemini AI code review API
```

---

## Projects

| Project | Description | Stack | Status |
|---------|-------------|-------|--------|
| [News Aggregator API](projects/news_aggregator/) | Async REST API that fetches, filters, and caches live news from NewsAPI.org | FastAPI, httpx, Pydantic | ✅ Complete |
| [Code Review AI API](projects/code_review_ai/) | AI-powered code review using Google Gemini — returns structured feedback with scores, issues, and suggestions | FastAPI, google-genai, Pydantic | ✅ Complete |

---

## Goals

- Build production-quality REST APIs with FastAPI
- Practice async programming with `httpx`
- Implement caching strategies
- Integrate third-party AI APIs (Google Gemini)
- Write clean, documented, and modular backends
