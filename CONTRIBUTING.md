# Contributing Guidelines

Thank you for exploring this portfolio! While this is primarily a personal portfolio project, feedback and suggestions are always welcome.

## Code Quality Standards

All code in this repository follows these standards:

### Python Projects
- ✅ Type hints on all functions and methods
- ✅ Comprehensive docstrings (Google style)
- ✅ pytest for testing (run with: `pytest tests/ -v`)
- ✅ Error handling with descriptive exceptions
- ✅ Logging instead of print statements
- ✅ SOLID principles and clean architecture

### JavaScript/React Projects
- ✅ Component-based architecture
- ✅ Props validation
- ✅ Modern ES6+ syntax
- ✅ Proper error boundaries
- ✅ Responsive design

## Project Structure

### Python Projects
```
project_name/
├── src/ or main files          # Source code
├── tests/                      # Unit & integration tests
├── requirements.txt            # Dependencies
├── README.md                   # Project documentation
├── .env.example               # Environment template
└── config.yml (optional)      # Configuration
```

### Frontend Projects
```
project_name/
├── src/
│   ├── components/            # React components
│   ├── pages/                 # Page components
│   ├── utils/                 # Utility functions
│   ├── App.jsx
│   └── main.jsx
├── public/                    # Static assets
├── package.json
├── vite.config.js
└── README.md
```

## Testing Requirements

Before submission/deployment:

### Python Projects
```bash
# Run all tests
pytest tests/ -v

# Check coverage
pytest tests/ --cov=src

# Type checking (if mypy is configured)
mypy src/
```

### Frontend Projects
```bash
# Build check
npm run build

# Linting (if configured)
npm run lint
```

## Security Considerations

- ✅ Never commit `.env` files (use `.env.example`)
- ✅ Never commit database files (`*.db`, `*.sqlite3`)
- ✅ Validate and sanitize user inputs
- ✅ Use environment variables for secrets/API keys
- ✅ Keep dependencies updated
- ✅ Review security advisories: `npm audit`, `pip-audit`

## Documentation

Every project should have:

1. **README.md** with:
   - Clear project description
   - Features list
   - Quick Start guide
   - Project structure
   - How to run tests
   - Links to documentation

2. **Docstrings** on every function/class:
   ```python
   def authenticate_user(username: str, password: str) -> bool:
       """
       Authenticate a user against the database.
       
       Args:
           username: The user's username (3-20 characters)
           password: The user's password (8-128 characters)
       
       Returns:
           bool: True if authentication successful, False otherwise
           
       Raises:
           ValueError: If username or password format is invalid
           AccountLockedError: If account is rate-limited
       """
   ```

3. **Type Hints** (Python):
   ```python
   from typing import Optional, List
   
   def process_data(items: List[str], count: Optional[int] = None) -> Dict[str, int]:
       """Process items and return results."""
   ```

## Performance Guidelines

- Avoid N+1 database queries
- Use async/await for I/O operations
- Implement caching where appropriate
- Profile code before optimizing
- Document performance implications of changes

## Reporting Issues

If you find issues or have suggestions:

1. Check if it's a known issue
2. Provide clear description and reproduction steps
3. Include environment details (Python version, OS, etc.)
4. Share relevant code snippets or logs

## Attribution

When using or referencing code from this portfolio:

- Give appropriate credit
- Link back to the original repository
- Include the MIT License

---

**Thank you for your interest in this portfolio!** 🚀
