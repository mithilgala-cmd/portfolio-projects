# Code Review AI — Frontend

AI-powered code review tool built with **React + Vite + Monaco Editor**. Paste code, select a language, and get a structured AI review powered by the Code Review AI backend.

---

## Features

- 🖊️ **Monaco Editor** — full VS Code-quality editor with syntax highlighting
- 🌐 **15+ languages** supported with automatic language detection in the editor
- 📊 **Overall quality score** (0–100) and complexity rating
- 🔴 **Issues sorted by severity** — errors → warnings → info, with expandable suggestions
- 💡 **Improvement suggestions** and positive feedback sections
- ⏳ **Loading state** — spinner while the AI processes the review

---

## Project Structure

```
code-review-ai/
├── src/
│   ├── components/
│   │   ├── LanguageSelector.jsx   # Language dropdown
│   │   ├── ReviewPanel.jsx        # Review results display
│   │   └── ScoreCard.jsx          # Score + complexity card
│   ├── App.jsx                    # Main layout and review logic
│   └── index.css                  # Dark-theme design system
├── package.json
└── vite.config.js
```

---

## Quick Start

### 1. Ensure the backend is running

The frontend expects the Code Review AI API at `http://localhost:8001`.

```bash
cd backend/projects/code_review_ai
pip install -r requirements.txt
uvicorn main:app --reload --port 8001
```

### 2. Run the frontend

```bash
cd frontend/code-review-ai
npm install
npm run dev
```

Visit `http://localhost:5173`.

---

## Tech Stack

- **React 19** + **Vite 8**
- **Monaco Editor** (`@monaco-editor/react`) — code editor
- **Axios** — HTTP requests to the backend
- **Lucide React** — icons
- **Vanilla CSS** — dark-theme design system

---

## Stack

![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat&logo=vite&logoColor=white)
![Monaco](https://img.shields.io/badge/Monaco%20Editor-0078D4?style=flat&logo=visual-studio-code&logoColor=white)
![Axios](https://img.shields.io/badge/Axios-5A29E4?style=flat)

---

> **Backend:** The FastAPI backend lives at `backend/projects/code_review_ai/`. Both services must be running for the app to work.
