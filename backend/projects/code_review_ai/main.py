import os
import json
import google.generativeai as genai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("GEMINI_API_KEY is not set. Add it to your .env file.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

app = FastAPI(
    title="CodeReview AI",
    description="AI-powered code review using Google Gemini",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ReviewRequest(BaseModel):
    code: str
    language: str


class Issue(BaseModel):
    severity: str      # "error" | "warning" | "info"
    category: str      # "bug" | "security" | "style" | "performance" | "logic"
    line: str | None   # e.g. "Line 12" or None if general
    description: str
    suggestion: str


class ReviewResponse(BaseModel):
    summary: str
    overall_score: int   # 0–100
    complexity: str      # "Low" | "Medium" | "High"
    issues: list[Issue]
    improvements: list[str]
    positive_points: list[str]


REVIEW_PROMPT_TEMPLATE = """
You are an expert senior software engineer performing a thorough code review.

Analyze the following {language} code and return a JSON object (no markdown, no code fences, raw JSON only) with this exact structure:

{{
  "summary": "<2-3 sentence overall summary of the code>",
  "overall_score": <integer 0-100, where 100 is perfect code>,
  "complexity": "<one of: Low | Medium | High>",
  "issues": [
    {{
      "severity": "<one of: error | warning | info>",
      "category": "<one of: bug | security | style | performance | logic>",
      "line": "<e.g. 'Line 12' or null if general>",
      "description": "<clear description of the issue>",
      "suggestion": "<concrete fix or improvement>"
    }}
  ],
  "improvements": ["<actionable improvement suggestion>", ...],
  "positive_points": ["<something done well>", ...]
}}

Rules:
- "error" severity = bugs, crashes, security vulnerabilities
- "warning" severity = code smells, performance issues, bad practices
- "info" severity = style, readability, minor suggestions
- improvements: max 5 bullet points of the most impactful changes
- positive_points: max 3 things done well (encourage the developer)
- Be specific and constructive. Reference actual code patterns.
- Return ONLY valid JSON, nothing else.

Code to review:
```{language}
{code}
```
"""


@app.get("/")
def root():
    return {"message": "CodeReview AI is running 🚀", "docs": "/docs"}


@app.post("/review", response_model=ReviewResponse)
async def review_code(request: ReviewRequest):
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty.")
    if len(request.code) > 10_000:
        raise HTTPException(status_code=400, detail="Code is too long. Maximum 10,000 characters.")

    prompt = REVIEW_PROMPT_TEMPLATE.format(
        language=request.language,
        code=request.code,
    )

    try:
        response = model.generate_content(prompt)
        raw_text = response.text.strip()

        # Strip markdown code fences if Gemini wraps them anyway
        if raw_text.startswith("```"):
            lines = raw_text.split("\n")
            raw_text = "\n".join(lines[1:-1])

        data = json.loads(raw_text)
        return ReviewResponse(**data)

    except json.JSONDecodeError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to parse AI response as JSON: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI review failed: {str(e)}")
