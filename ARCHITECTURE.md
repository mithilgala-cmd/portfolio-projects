# Project Architecture & Design Patterns

This document outlines the architectural decisions, design patterns, and technical trade-offs across all projects in this portfolio.

## Table of Contents
- [Secure Chat Application](#secure-chat-application)
- [APIs (News Aggregator & Code Review)](#apis-news-aggregator--code-review)
- [Machine Learning Pipeline](#machine-learning-pipeline)
- [Frontend Applications](#frontend-applications)
- [DSA Library](#dsa-library)

---

## Secure Chat Application

### Architecture Overview

```
┌─────────────────────────────────────────────────┐
│            Client Application                   │
│  • Generate RSA-2048 keypair                   │
│  • Generate AES session keys                   │
│  • Encrypt messages with AES                  │
│  • Sign with private key (optional)             │
└────────────────┬────────────────────────────────┘
                 │ (Encrypted Messages + Public Key)
┌────────────────▼────────────────────────────────┐
│            Chat Server (Port 65432)             │
│  • Multi-threaded client handling              │
│  • Authenticate users (rate-limited)           │
│  • Message relay (blind relay - can't decrypt) │
│  • Public key exchange                          │
└────────────────┬────────────────────────────────┘
                 │ (Encrypted Storage)
┌────────────────▼────────────────────────────────┐
│           SQLite Database                       │
│  • User credentials (PBKDF2-hashed)           │
│  • Rate limiting state (lockout times)        │
│  • Audit trails (login attempts, errors)      │
└─────────────────────────────────────────────────┘
```

### Key Design Decisions

#### 1. Server-Blind E2E Encryption
- **Decision:** Server cannot decrypt message content
- **Why:** Ensures privacy even if server is compromised
- **Trade-off:** Client must handle encryption/decryption overhead
- **Benefit:** Single source of truth: endpoints own their keys

#### 2. Choice of Cryptography
- **RSA-2048 for Key Exchange:** Industry standard, well-tested
- **AES-256-CBC for Messages:** Fast symmetric encryption
- **PBKDF2 for Passwords:** Memory-hard hashing (100,000 iterations)
- **Why:** Balance between security and performance

#### 3. Rate Limiting Strategy
- **Implementation:** 5-attempt lockout with 5-minute blocks
- **Storage:** SQLite with timestamps
- **Why:** Prevents brute-force without complex infrastructure
- **Scalability:** Can migrate to Redis for horizontally-scaled servers

#### 4. Multi-threaded Server
- **One thread per client:** Simple model, handles ~1000 concurrent clients
- **Thread-safe database access:** SQLite with proper connection handling
- **Why:** Simpler than async, sufficient for demonstration
- **Limitation:** Not suitable for 10k+ concurrent clients

### Code Organization
```
Cybersecurity/
├── crypto/              # Encryption modules
│   ├── aes.py          # AES-256-CBC implementation
│   ├── rsa.py          # RSA-2048 key exchange
│   ├── hash.py         # PBKDF2-SHA256 hashing
│   └── e2e.py          # End-to-end encryption wrapper
├── auth/               # Authentication & rate limiting
│   └── auth.py         # User auth with rate limiting
├── server/             # Chat server
│   └── server.py       # Multi-threaded server
├── client/             # CLI client
│   └── client.py       # Interactive chat client
├── utils/              # Utilities
│   ├── config.py       # Configuration management
│   ├── db.py          # SQLite database abstraction
│   └── logger.py       # Logging setup
├── tests/              # Unit tests (22 total)
│   ├── test_crypto.py
│   ├── test_auth.py
│   └── test_server.py
└── web/                # Flask web interface (optional)
```

### Security Properties Verified
- ✅ **Confidentiality:** Only endpoints can decrypt messages
- ✅ **Integrity:** CBC mode + PKCS7 padding
- ✅ **Authenticity:** Can verify sender with public key
- ✅ **Availability:** Rate limiting prevents DOS attacks
- ✅ **Auditability:** Full logging for compliance

---

## APIs (News Aggregator & Code Review)

### Architecture Overview

```
┌─────────────────────────────────┐
│     Client (Browser/App)        │
│   • Makes HTTP requests         │
│   • Parses JSON responses        │
└────────────┬────────────────────┘
             │ HTTP/CORS
┌────────────▼────────────────────┐
│  FastAPI Application            │
│  ├── Input Validation (Pydantic)│
│  ├── Business Logic             │
│  ├── Caching Layer (TTL)        │
│  └── Error Handling             │
└────────────┬────────────────────┘
             │ External API Calls
┌────────────▼────────────────────┐
│  External Services              │
│  • NewsAPI.org                  │
│  • Google Gemini API            │
└─────────────────────────────────┘
```

### Design Patterns Used

#### 1. Async/Await Pattern
```python
@app.get("/news/top-headlines")
async def get_top_headlines(country: str, category: str) -> NewsResponse:
    # Non-blocking I/O operation
    result = await fetch_from_newsapi(country, category)
    return result
```
- **Why:** High concurrency, non-blocking I/O
- **Enables:** Single server handling 100+ concurrent requests

#### 2. In-Memory Caching with TTL
```python
class Cache:
    def __init__(self, ttl_minutes: int):
        self.data = {}
        self.ttl = ttl_minutes * 60
        
    async def get(self, key: str) -> Optional[Any]:
        if key in self.data:
            if time.time() - self.data[key]['time'] < self.ttl:
                return self.data[key]['value']
        return None
```
- **Why:** Reduce external API calls, improve response time
- **Trade-off:** Memory usage ~100MB for typical usage

#### 3. Pydantic for Validation
```python
class NewsArticle(BaseModel):
    title: str
    description: Optional[str] = None
    content: str
    url: HttpUrl
    publishedAt: datetime
    
    class Config:
        json_schema_extra = {
            "example": {
                "title": "Breaking News Article",
                "content": "Article content..."
            }
        }
```
- **Why:** Automatic validation, serialization, documentation
- **Benefit:** OpenAPI/Swagger docs automatically generated

#### 4. Router-Based Modularization
```
src/
├── routers/
│   ├── health.py      # GET /health
│   └── news.py        # GET /news/* endpoints
├── main.py            # App initialization, CORS
├── models.py          # Pydantic schemas
├── fetcher.py         # External API client
└── cache.py           # Caching logic
```
- **Why:** Easy to scale, test, and maintain
- **Enables:** Adding new endpoints without touching main.py

### Configuration Management
- **Environment Variables** (`.env` file):
  - API keys, base URLs, timeouts
  - Loaded at startup with sensible defaults
- **YAML Config** (`config.yml`):
  - Feature flags, cache TTL, rate limits
  - Hot-reloadable (custom implementation)

---

## Machine Learning Pipeline

### Architecture Overview

```
Raw Data
   │
   ▼
┌─────────────────────────┐
│ EDA & Exploration       │
│ (Jupyter Notebooks)     │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Data Preprocessing      │
│ • Missing value imputation
│ • Feature scaling       │
│ • Categorical encoding  │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Train/Test Split        │
│ (No data leakage)       │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Model Training          │
│ • Cross-validation      │
│ • Hyperparameter tuning │
│ • Model comparison      │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│ Evaluation & Results    │
│ • R² score              │
│ • RMSE, MAE             │
│ • Test set performance  │
└────────┬────────────────┘
         │
         ▼
Trained Model + Predictions
```

### Design Decisions

#### 1. Scikit-learn Pipelines
```python
pipeline = Pipeline([
    ('preprocessor', ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(), categorical_features)
        ]
    )),
    ('model', Ridge(alpha=1.0))
])
```
- **Why:** Prevents data leakage, reproducible preprocessing
- **Benefit:** Single `.fit()` call handles everything

#### 2. 5-Fold Cross-Validation
```python
scores = cross_val_score(
    pipeline, X_train, y_train,
    cv=5,
    scoring='r2'
)
```
- **Why:** More robust evaluation than single train/test split
- **Result:** Average of 5 models, variance estimates

#### 3. Not Over-Engineering
- **Decision:** Use simple models first (Linear Regression)
- **Trade-off:** Sacrifice 2-3% accuracy for interpretability
- **Justification:** Simple model outperformed Random Forest on test set

### File Organization
```
house_price_prediction/
├── src/
│   ├── data_preprocessing.py   # Preprocessing pipeline
│   ├── train.py               # Model training
│   ├── predict.py             # Inference
│   └── evaluate.py            # Metrics & analysis
├── notebooks/
│   └── eda.ipynb              # Exploratory analysis
├── data/
│   ├── train.csv              # Training data
│   └── test.csv               # Test data
├── models/
│   └── best_model.pkl         # Serialized model
├── logs/
│   └── training.log           # Training logs
├── config.yml                 # Hyperparameters
└── requirements.txt
```

### Reproducibility
- ✅ Fixed random seeds
- ✅ Train/test split before preprocessing
- ✅ Pipeline serialization (pickle)
- ✅ Logged hyperparameters and results

---

## Frontend Applications

### Architecture Overview

```
React Component Tree
├── App.jsx (Main router)
├── Pages/
│   ├── HomePage
│   ├── ListPage
│   └── DetailsPage
├── Components/ (Reusable)
│   ├── ArticleCard
│   ├── SearchBar
│   └── Pagination
└── Utils/
    ├── apiClient.js
    └── formatters.js
```

### Design Patterns

#### 1. Component Composition
```jsx
export function NewsCard({ article, onSelect }) {
    return (
        <div className="card">
            <h3>{article.title}</h3>
            <p>{article.description}</p>
            <button onClick={() => onSelect(article)}>Read More</button>
        </div>
    );
}
```
- **Why:** Reusable, testable, single responsibility
- **Benefit:** Easy to style consistently

#### 2. Custom Hooks for Logic
```javascript
function useNewsApi(url, dependencies) {
    const [data, setData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    
    useEffect(() => {
        fetchData();
    }, dependencies);
    
    return { data, loading, error };
}
```
- **Why:** Shared logic across components
- **Benefit:** Easy to test and maintain

#### 3. Environment-Based Configuration
```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```
- **Why:** Different endpoints for dev/prod
- **Enables:** Easy deployment to different environments

### Build & Deployment
- **Vite** for build tooling
  - Fast development server (HMR)
  - Optimized production builds
  - Code splitting automatic
- **Output:** Static files ready for CDN/static hosting

---

## DSA Library

### Structure & Organization

```
dsa-patterns-python-1/
├── arrays/                  # Array-based problems
├── linked_list/            # Linked list problems
├── trees/                  # Tree/BST problems
├── graphs/                 # Graph/traversal problems
├── dynamic_programming/    # DP problems
├── backtracking/           # Backtracking problems
├── tests/                  # Mirror structure with tests
│   ├── arrays/test_*.py
│   ├── trees/test_*.py
│   └── ...
├── template.py             # Solution template
├── pytest.ini
└── requirements.txt
```

### Design Principles

#### 1. Problem-Focused Organization
- Each file = one related problem area
- Consistent naming: `problem_name.py`
- Each implements: solution + complexity analysis

#### 2. Comprehensive Testing
```python
# tests/arrays/test_two_sum.py
def test_two_sum_basic():
    result = two_sum([2, 7, 11, 15], 9)
    assert result == [0, 1]

def test_two_sum_edge_cases():
    assert two_sum([1], 1) is None  # Not enough elements
```
- **Coverage:** All edge cases tested
- **Documentation:** Each test documents expected behavior

#### 3. Complexity Analysis
```python
def two_sum(nums: List[int], target: int) -> Optional[List[int]]:
    """
    Two Sum using hash map.
    
    Time Complexity: O(n) - single pass through array
    Space Complexity: O(n) - hash map storage
    """
```
- **Why:** Essential for interview preparation
- **Included:** Both time and space analysis

#### 4. Solution Template
```python
# template.py - guides implementation
def solution(problem):
    """
    1. Understand the problem
    2. Design approach (discuss trade-offs)
    3. Implement efficiently
    4. Verify with examples
    5. Analyze complexity
    """
```

---

## Cross-Cutting Concerns

### Error Handling Strategy

#### Python Projects
```python
try:
    # Business logic
except ValueError as e:
    logger.error(f"Invalid input: {e}")
    raise
except DatabaseError as e:
    logger.error(f"Database operation failed: {e}")
    # Graceful failure
except Exception as e:
    logger.exception(f"Unexpected error: {e}")
    raise
```

#### JavaScript/React Projects
```javascript
try {
    const response = await fetch(url);
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    return await response.json();
} catch (error) {
    console.error('API Error:', error);
    throw error;
}
```

### Logging Standards
- **Level Usage:**
  - `DEBUG`: Detailed flow information
  - `INFO`: Significant events (startup, user actions)
  - `WARNING`: Unexpected situations (rate limited user)
  - `ERROR`: Recoverable errors (failed API call)
  - `CRITICAL`: System failures (database down)

### Testing Pyramid
```
        ▲
       / \
      /   \ E2E Tests (10%)
     /     \
    /-------\
   /         \ Integration Tests (30%)
  /           \
 /─────────────\
/               \ Unit Tests (60%)
```

---

## Technology Choices & Justifications

| Choice | Alternative | Why This One |
|--------|-------------|--------------|
| FastAPI | Django, Flask | Async-first, modern, fast |
| React | Vue, Svelte | Larger ecosystem, more jobs |
| SQLite | PostgreSQL | No server needed for demo, sufficient for scale |
| RSA-2048 | ECC, 4096-bit | Balance security and performance |
| Scikit-learn | TensorFlow, PyTorch | Simpler than deep learning, sufficient for regression |
| Pytest | unittest | More Pythonic, better fixtures, cleaner syntax |

---

## Future Improvements

### Cybersecurity Project
- [ ] WebSocket support for real-time chat
- [ ] Redis for horizontal scaling
- [ ] TLS for transport layer
- [ ] Multi-password accounts

### APIs
- [ ] GraphQL endpoint
- [ ] Rate limiting per user/IP
- [ ] Database persistence (PostgreSQL)
- [ ] Message queuing (Redis/RabbitMQ)

### ML Pipeline
- [ ] Neural network approach
- [ ] Automated hyperparameter tuning
- [ ] Model serving (Flask/FastAPI)
- [ ] Retraining pipeline

### Frontend
- [ ] Dark mode support
- [ ] Offline functionality
- [ ] Mobile-optimized UI
- [ ] Real-time updates (WebSocket)

---

**Last Updated:** April 2026  
**Author:** Mithil Gala  
