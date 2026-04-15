# crypto/hash.py
"""
Password hashing module using PBKDF2-SHA256.
Provides secure password hashing with salt generation and verification.
"""

import hashlib
import os
from utils.config import SALT_SIZE, HASH_ITERATIONS


def generate_salt() -> bytes:
    """Generate a random salt for password hashing."""
    return os.urandom(SALT_SIZE)


def hash_password(password: str, salt: bytes = None) -> tuple[str, str]:
    """Hash a password using PBKDF2-SHA256."""
    if salt is None:
        salt = generate_salt()
    
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        HASH_ITERATIONS
    )
    
    return hashed.hex(), salt.hex()


def verify_password(password: str, hashed_password_hex: str, salt_hex: str) -> bool:
    """Verify password against stored PBKDF2 hash with constant-time comparison."""
    salt = bytes.fromhex(salt_hex)
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        HASH_ITERATIONS
    )
    return hashed.hex() == hashed_password_hex
