# Code Review AI API

A FastAPI backend that accepts source code and language, calls Gemini, and returns a structured review JSON.

## Features

- `POST /review` endpoint for AI code review
- Structured output: summary, score, complexity, issues, improvements
- Input validation and error handling
- CORS enabled for local frontend integration

## Tech Stack

- Python
- FastAPI
- Google Gemini API (`gemini-2.0-flash`)
- Pydantic

## Run Locally

```bash
cd backend/projects/code_review_ai
pip install -r requirements.txt
copy .env.example .env
```

Add your key in `.env`:

```env
GEMINI_API_KEY=your_key_here
```

Start the server:

```bash
uvicorn main:app --reload --port 8001
```

Docs: `http://127.0.0.1:8001/docs`

## API Contract

### `POST /review`

Request body:

```json
{
  "code": "def add(a, b): return a + b",
  "language": "python"
}
```

Returns a structured review object containing quality score and actionable feedback.

## Notes

- This project depends on an external LLM provider and API key.
- If the model response is not valid JSON, the API returns a 500 with parse details.
