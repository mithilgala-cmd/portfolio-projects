"""Authentication module with rate limiting and password verification.

Production-ready authentication with persistent storage support.
Uses SQLite database for credential storage with fallback to in-memory for testing.
"""

import sys
import os
import time
import logging
from typing import Dict, Tuple

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crypto.hash import hash_password, verify_password
from utils.db import get_db

logger = logging.getLogger(__name__)

# Legacy in-memory store for backward compatibility and testing
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
    db = get_db()
    user = db.get_user(username)
    
    if not user:
        return False
    
    if user.get("attempts", 0) >= MAX_ATTEMPTS:
        elapsed = time.time() - user.get("last_attempt", 0)
        if elapsed < LOCKOUT_DURATION:
            return True
        # Auto-unlock if lockout period expired
        db.reset_failed_attempts(username)
    
    return False


def register_user(username: str, password: str) -> Tuple[bool, str]:
    """Register new user with validation and persistent storage."""
    if not is_valid_username(username):
        return False, "Invalid username. Use 3-20 alphanumeric/underscore characters."
    
    if not is_valid_password(password):
        return False, "Invalid password. Use 8-128 characters."
    
    db = get_db()
    if db.user_exists(username):
        return False, "Registration failed."
    
    hashed_pwd, salt = hash_password(password)
    
    success = db.create_user(username, hashed_pwd, salt)
    if success:
        # Also keep in-memory store for backward compatibility
        USER_STORE[username] = {
            "hash": hashed_pwd,
            "salt": salt,
            "attempts": 0,
            "last_attempt": 0
        }
        return True, "Success"
    
    return False, "Registration failed."


def authenticate_user(username: str, password: str) -> Tuple[bool, str]:
    """Authenticate user with rate limiting protection and persistent storage."""
    if is_account_locked(username):
        return False, "Authentication failed."
    
    db = get_db()
    user_data = db.get_user(username)
    
    if not user_data:
        return False, "Authentication failed."
    
    if verify_password(password, user_data["hash"], user_data["salt"]):
        # Successful login - reset attempts
        db.reset_failed_attempts(username)
        logger.info(f"User '{username}' authenticated successfully")
        return True, "Success"
    else:
        # Failed login - increment attempts
        attempts = user_data.get("attempts", 0) + 1
        last_attempt = time.time()
        db.update_failed_attempts(username, attempts, last_attempt)
        logger.warning(f"Failed login attempt for user '{username}' (attempt {attempts}/{MAX_ATTEMPTS})")
        return False, "Authentication failed."


# Database management functions for production use
def get_all_users() -> list:
    """Get all registered users (admin function)."""
    db = get_db()
    return db.get_all_users()


def delete_user(username: str) -> bool:
    """Delete user from database (admin function)."""
    db = get_db()
    if username in USER_STORE:
        del USER_STORE[username]
    return db.delete_user(username)


def user_exists(username: str) -> bool:
    """Check if user exists in database."""
    db = get_db()
    return db.user_exists(username)

