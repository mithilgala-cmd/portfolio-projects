# auth/auth.py
"""
Authentication module for user registration and login.
Provides secure password verification and user management.
"""

import sys
import os
import time
from typing import Dict, Tuple

# Add parent directory to path so we can import crypto.hash
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crypto.hash import hash_password, verify_password

# In-memory user store. In production, use a database!
# Format: username: {"hash": "...", "salt": "...", "attempts": int, "last_attempt": float}
USER_STORE: Dict[str, Dict] = {}

# Rate limiting configuration
MAX_ATTEMPTS = 5
LOCKOUT_DURATION = 300  # 5 minutes in seconds


def is_valid_username(username: str) -> bool:
    """
    Validate username format.
    
    Args:
        username (str): Username to validate.
    
    Returns:
        bool: True if username is valid, False otherwise.
    
    Username requirements:
        - Length: 3-20 characters
        - Alphanumeric and underscore only
    """
    if not username or len(username) < 3 or len(username) > 20:
        return False
    return username.isalnum() or all(c.isalnum() or c == '_' for c in username)


def is_valid_password(password: str) -> bool:
    """
    Validate password strength.
    
    Args:
        password (str): Password to validate.
    
    Returns:
        bool: True if password meets requirements, False otherwise.
    
    Password requirements:
        - Minimum length: 8 characters
        - Maximum length: 128 characters
    """
    return password and 8 <= len(password) <= 128


def is_account_locked(username: str) -> bool:
    """
    Check if account is locked due to too many login attempts.
    
    Args:
        username (str): Username to check.
    
    Returns:
        bool: True if account is locked, False otherwise.
    """
    if username not in USER_STORE:
        return False
    
    user = USER_STORE[username]
    if user.get("attempts", 0) >= MAX_ATTEMPTS:
        elapsed = time.time() - user.get("last_attempt", 0)
        if elapsed < LOCKOUT_DURATION:
            return True
        else:
            # Reset attempts after lockout duration
            user["attempts"] = 0
    
    return False


def register_user(username: str, password: str) -> Tuple[bool, str]:
    """
    Register a new user with input validation.
    
    Args:
        username (str): Desired username.
        password (str): Desired password.
    
    Returns:
        Tuple[bool, str]: (success: bool, message: str)
            - (True, "Success") if registration succeeds
            - (False, message) with error description if it fails
    
    Validation:
        - Username and password must be valid format
        - Username must not already exist
    """
    # Validate inputs
    if not is_valid_username(username):
        return False, "Invalid username. Use 3-20 alphanumeric/underscore characters."
    
    if not is_valid_password(password):
        return False, "Invalid password. Use 8-128 characters."
    
    # Check if user already exists
    if username in USER_STORE:
        return False, "Registration failed."  # Don't leak that user exists
    
    # Hash and store password
    hashed_pwd, salt = hash_password(password)
    USER_STORE[username] = {
        "hash": hashed_pwd,
        "salt": salt,
        "attempts": 0,
        "last_attempt": 0
    }
    
    return True, "Success"


def authenticate_user(username: str, password: str) -> Tuple[bool, str]:
    """
    Authenticate a user with rate limiting protection.
    
    Args:
        username (str): Username.
        password (str): Password.
    
    Returns:
        Tuple[bool, str]: (success: bool, message: str)
            - (True, "Success") if authentication succeeds
            - (False, message) with generic error message if it fails
    
    Features:
        - Rate limiting: Locks account for LOCKOUT_DURATION after MAX_ATTEMPTS failures
        - Generic error messages to prevent username enumeration
    """
    # Check if account is locked
    if is_account_locked(username):
        return False, "Authentication failed."  # Generic message
    
    # Check if user exists
    if username not in USER_STORE:
        return False, "Authentication failed."  # Generic message
    
    user_data = USER_STORE[username]
    
    # Verify password
    if verify_password(password, user_data["hash"], user_data["salt"]):
        # Reset failed attempts on successful login
        user_data["attempts"] = 0
        user_data["last_attempt"] = 0
        return True, "Success"
    else:
        # Increment failed attempts
        user_data["attempts"] = user_data.get("attempts", 0) + 1
        user_data["last_attempt"] = time.time()
        return False, "Authentication failed."  # Generic message
