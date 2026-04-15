# crypto/hash.py
"""
Password hashing module using PBKDF2-SHA256.
Provides secure password hashing with salt generation and verification.
"""

import hashlib
import os
from utils.config import SALT_SIZE, HASH_ITERATIONS


def generate_salt() -> bytes:
    """
    Generate a random salt for password hashing.
    
    Returns:
        bytes: Cryptographically random salt of SALT_SIZE bytes.
    """
    return os.urandom(SALT_SIZE)


def hash_password(password: str, salt: bytes = None) -> tuple[str, str]:
    """
    Hash a password using PBKDF2-SHA256 with salting.
    
    Uses PBKDF2 with SHA256 for key derivation, which is resistant to
    dictionary and brute-force attacks due to its computational cost.
    
    Args:
        password (str): Plain-text password to hash.
        salt (bytes, optional): Salt bytes. If None, a new salt is generated.
    
    Returns:
        tuple[str, str]: (hashed_password_hex, salt_hex) both as hex strings.
    
    Note:
        Uses HASH_ITERATIONS rounds for increased security against
        brute-force attacks (configurable in utils.config).
    """
    if salt is None:
        salt = generate_salt()
    
    # Use PBKDF2 with SHA-256 for key derivation
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        HASH_ITERATIONS
    )
    
    return hashed.hex(), salt.hex()


def verify_password(password: str, hashed_password_hex: str, salt_hex: str) -> bool:
    """
    Verify a plain-text password against a stored hash and salt.
    
    Args:
        password (str): Plain-text password to verify.
        hashed_password_hex (str): Stored password hash as hex string.
        salt_hex (str): Stored salt as hex string.
    
    Returns:
        bool: True if password is correct, False otherwise.
    """
    salt = bytes.fromhex(salt_hex)
    hashed = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode('utf-8'),
        salt,
        HASH_ITERATIONS
    )
    return hashed.hex() == hashed_password_hex
