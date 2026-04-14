# auth/auth.py
import sys
import os

# Add parent directory to path so we can import crypto.hash
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crypto.hash import hash_password, verify_password

# In-memory user store. In production, use a database!
# Format: username: {"hash": "...", "salt": "..."}
USER_STORE = {}

def register_user(username: str, password: str) -> bool:
    """Register a new user if they don't already exist."""
    if username in USER_STORE:
        return False # User already exists
    
    hashed_pwd, salt = hash_password(password)
    USER_STORE[username] = {
        "hash": hashed_pwd,
        "salt": salt
    }
    return True

def authenticate_user(username: str, password: str) -> bool:
    """Authenticate returning True if valid."""
    if username not in USER_STORE:
        return False
    
    user_data = USER_STORE[username]
    return verify_password(password, user_data["hash"], user_data["salt"])
