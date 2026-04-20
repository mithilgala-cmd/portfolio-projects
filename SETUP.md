# 🚀 Complete Setup Guide

This guide walks you through setting up and running all projects in this portfolio.

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Global Setup](#global-setup)
3. [Project-Specific Setup](#project-specific-setup)
4. [Running Tests](#running-tests)
5. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required
- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 16+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)

### Verify Installation
```bash
python --version     # Should be 3.10+
node --version      # Should be 16+
npm --version       # Usually comes with Node.js
git --version
```

---

## Global Setup

### 1. Clone the Repository
```bash
git clone https://github.com/mithilgala-cmd/portfolio-projects.git
cd portfolio-projects
```

### 2. Create Python Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Verify Environment
```bash
python -m pip install --upgrade pip
pip --version
```

---

## Project-Specific Setup

### 🛡️ Cybersecurity Project

**Security features:** E2E encryption, authentication, rate limiting

```bash
# Navigate to project
cd Cybersecurity

# Install dependencies
pip install -r requirements.txt

# Run the demo
python demo_run.py

# Run tests
pytest tests/ -v

# Run with custom settings
python demo_run.py --help
```

**What it demonstrates:**
- ✅ RSA-2048 key exchange
- ✅ AES-256-CBC encryption
- ✅ PBKDF2 password hashing
- ✅ Rate limiting & account lockout
- ✅ SQLite persistence
- ✅ Multi-threaded server
- ✅ Type hints & comprehensive logging

---

### 🌐 News Aggregator API

**REST API for news aggregation with caching**

```bash
# Navigate to project
cd backend/projects/news_aggregator

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env and add your NewsAPI.org key
# (Get free key at https://newsapi.org/register)
# NEWSAPI_KEY=your_api_key_here

# Run the server
uvicorn main:app --reload --port 8000

# Access API docs
# Visit: http://localhost:8000/docs
```

**API Endpoints:**
- `GET /docs` - Interactive API documentation
- `GET /health` - Health check
- `GET /news/top-headlines` - Top headlines
- `GET /news/search` - Search news
- `GET /news/sources` - Available sources

---

### 🤖 Code Review AI API

**AI-powered code review using Google Gemini**

```bash
# Navigate to project
cd backend/projects/code_review_ai

# Install dependencies
pip install -r requirements.txt

# Create environment file
cp .env.example .env

# Edit .env and add your Google Gemini API key
# (Get free key at https://aistudio.google.com/app/apikey)
# GEMINI_API_KEY=your_api_key_here

# Run the server
uvicorn main:app --reload --port 8001

# Access API docs
# Visit: http://localhost:8001/docs
```

**API Endpoints:**
- `GET /docs` - Interactive API documentation
- `POST /review` - Submit code for review
- `GET /status` - API status

---

### 💻 Frontend Projects

#### News Aggregator UI
```bash
cd frontend/news-aggregator

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Visit: http://localhost:5173
```

#### Code Review AI UI
```bash
cd frontend/code-review-ai

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Visit: http://localhost:5173
```

**Note:** Make sure the backend APIs are running on the expected ports.

---

### 🤖 House Price Prediction (ML)

**Full machine learning pipeline with Kaggle data**

```bash
# Navigate to project
cd machine_learning/projects/house_price_prediction

# Install dependencies
pip install -r requirements.txt

# Download data (automatic or manual from Kaggle)
# Place training data in: data/train.csv
# Place test data in: data/test.csv

# Run training
python src/train.py

# Run predictions
python src/predict.py

# Explore with Jupyter
jupyter notebook notebooks/eda.ipynb
```

**Output:**
- Trained models saved to `models/`
- Predictions saved to `data/predictions.csv`
- Logs to `logs/`

---

### 📚 DSA Patterns Library

**25+ algorithms with comprehensive test suite**

```bash
# Navigate to project
cd dsa-patterns-python-1

# Install dependencies (pytest for testing)
pip install -r requirements.txt

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/arrays/ -v

# Run with coverage
pytest tests/ --cov=. --cov-report=html

# View coverage report
# Open: htmlcov/index.html
```

**Categories:**
- Arrays & Strings
- Linked Lists
- Trees & Binary Search Trees
- Graphs & Graph Traversal
- Dynamic Programming
- Backtracking
- Heaps & Priority Queues
- Bit Manipulation
- And more...

---

## Running Tests

### Run All Tests
```bash
# Cybersecurity tests
cd Cybersecurity
pytest tests/ -v

# DSA tests
cd dsa-patterns-python-1
pytest tests/ -v
```

### Test Coverage
```bash
# Generate coverage report
pytest tests/ --cov=. --cov-report=html

# View report
open htmlcov/index.html  # macOS
start htmlcov/index.html # Windows
```

---

## Troubleshooting

### Python Issues

**Error: `python: command not found`**
- Ensure Python is installed and added to PATH
- Try: `python3` instead of `python`

**Error: `pip: command not found`**
- Try: `python -m pip` instead of `pip`

**Error: `ModuleNotFoundError`**
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`

### API Issues

**Error: `Port already in use`**
```bash
# Use a different port
uvicorn main:app --reload --port 8080
```

**Error: `API key invalid`**
- Check `.env` file exists (copy from `.env.example`)
- Verify API key is correct
- Check API key permissions/quotas

### Frontend Issues

**Error: `Module not found`**
```bash
# Clear and reinstall
rm -rf node_modules package-lock.json
npm install
```

**Error: `Port 5173 in use`**
```bash
# Vite will use the next available port automatically
npm run dev
```

### Database Issues

**Error: `Database locked` (SQLite)**
- Close other connections to the database
- Cybersecurity project locks `secure_chat.db`
- Ensure only one instance of the server is running

---

## Environment Variables Reference

### Cybersecurity Project
```bash
# No API keys needed - uses local SQLite
```

### News Aggregator API
```bash
NEWSAPI_KEY=your_newsapi_key_here
NEWSAPI_BASE_URL=https://newsapi.org/v2
CACHE_TTL_MINUTES=30
```

### Code Review AI API
```bash
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

---

## Quick Start (All Projects)

Run this to set everything up:

```bash
# Terminal 1: Cybersecurity
cd Cybersecurity
python demo_run.py

# Terminal 2: News Aggregator API
cd backend/projects/news_aggregator
uvicorn main:app --reload --port 8000

# Terminal 3: Code Review AI API
cd backend/projects/code_review_ai
uvicorn main:app --reload --port 8001

# Terminal 4: Frontend (pick one)
cd frontend/news-aggregator
npm install && npm run dev

# Terminal 5: Run tests
cd dsa-patterns-python-1
pytest tests/ -v
```

---

## Next Steps

1. ✅ Install all dependencies
2. ✅ Run individual project demos
3. ✅ Explore the code
4. ✅ Run the test suites
5. ✅ Check the documentation
6. ✅ Try modifying and extending projects

---

## Getting Help

- Check individual project `README.md` files
- Review the main [README.md](README.md)
- Check `docs/` folders for detailed documentation
- Review the code - it's well-commented!

---

**Happy exploring!** 🚀
