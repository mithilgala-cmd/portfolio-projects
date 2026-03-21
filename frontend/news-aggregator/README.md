# News Aggregator — Frontend

A React frontend for the [News Aggregator API](../../backend/projects/news_aggregator/) — browse top headlines and search for articles with a clean card-based layout.

---

## Features

- 🔍 **Search** articles by keyword
- 📰 **Top headlines** — latest news loaded on startup
- 🗂️ **News cards** — title, source, published date, and description
- ⏳ **Loading state** — spinner while fetching articles
- 🔗 **Read more links** — open full articles in a new tab

---

## Project Structure

```
news-aggregator/
├── src/
│   ├── components/
│   │   ├── Loader.jsx       # Loading spinner
│   │   └── NewsCard.jsx     # Individual article card
│   ├── App.jsx              # Main layout, search, fetch logic
│   ├── App.css
│   └── index.css
├── package.json
└── vite.config.js
```

---

## Quick Start

### 1. Start the backend first

The frontend expects the News Aggregator API running at `http://localhost:8000`.

```bash
cd backend/projects/news_aggregator
pip install -r requirements.txt
uvicorn src.main:app --reload
```

### 2. Run the frontend

```bash
cd frontend/news-aggregator
npm install
npm run dev
```

Visit `http://localhost:5173`.

---

## Tech Stack

- **React 19** + **Vite 8**
- **Lucide React** — icons
- **Vanilla CSS** — custom styling

---

## Stack

![React](https://img.shields.io/badge/React-61DAFB?style=flat&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-646CFF?style=flat&logo=vite&logoColor=white)
![CSS](https://img.shields.io/badge/CSS-1572B6?style=flat&logo=css3&logoColor=white)
