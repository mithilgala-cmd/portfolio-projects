"""Authentication module with rate limiting and password verification."""

import sys
import os
import time
from typing import Dict, Tuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crypto.hash import hash_password, verify_password

USER_STORE: Dict[str, Dict] = {}

MAX_ATTEMPTS = 5
LOCKOUT_DURATION = 300


def is_valid_username(username: str) -> bool:
    """Validate username: 3-20 chars, alphanumeric and underscore."""
    if not username or len(username) < 3 or len(username) > 20:
        return False
    return username.isalnum() or all(c.isalnum() or c == "_" for c in username)


def is_valid_password(password: str) -> bool:
    """Validate password: 8-128 characters."""
    return password and 8 <= len(password) <= 128


def is_account_locked(username: str) -> bool:
    """Check if account is locked due to failed login attempts."""
    if username not in USER_STORE:
        return False
    
    user = USER_STORE[username]
    if user.get("attempts", 0) >= MAX_ATTEMPTS:
        elapsed = time.time() - user.get("last_attempt", 0)
        if elapsed < LOCKOUT_DURATION:
            return True
        user["attempts"] = 0
    
    return False


def register_user(username: str, password: str) -> Tuple[bool, str]:
    """Register new user with validation."""
    if not is_valid_username(username):
        return False, "Invalid username. Use 3-20 alphanumeric/underscore characters."
    
    if not is_valid_password(password):
        return False, "Invalid password. Use 8-128 characters."
    
    if username in USER_STORE:
        return False, "Registration failed."
    
    hashed_pwd, salt = hash_password(password)
    USER_STORE[username] = {
        "hash": hashed_pwd,
        "salt": salt,
        "attempts": 0,
        "last_attempt": 0
    }
    
    return True, "Success"


def authenticate_user(username: str, password: str) -> Tuple[bool, str]:
    """Authenticate user with rate limiting protection."""
    if is_account_locked(username):
        return False, "Authentication failed."
    
    if username not in USER_STORE:
        return False, "Authentication failed."
    
    user_data = USER_STORE[username]
    
    if verify_password(password, user_data["hash"], user_data["salt"]):
        user_data["attempts"] = 0
        user_data["last_attempt"] = 0
        return True, "Success"
    else:
        user_data["attempts"] = user_data.get("attempts", 0) + 1
        user_data["last_attempt"] = time.time()
        return False, "Authentication failed."
