# crypto/hash.py
import hashlib
import os

def generate_salt() -> bytes:
    """Generate a random salt for password hashing."""
    return os.urandom(16)

def hash_password(password: str, salt: bytes = None) -> tuple[str, str]:
    """
    Hash a password using SHA-256 with HMAC/salting.
    Returns (hashed_password_hex, salt_hex)
    """
    if salt is None:
        salt = generate_salt()
    
    # Use SHA-256 with salt
    hasher = hashlib.sha256()
    hasher.update(salt + password.encode('utf-8'))
    
    return hasher.hexdigest(), salt.hex()

def verify_password(password: str, hashed_password_hex: str, salt_hex: str) -> bool:
    """Verify a plain-text password against the stored hash and salt."""
    salt = bytes.fromhex(salt_hex)
    hasher = hashlib.sha256()
    hasher.update(salt + password.encode('utf-8'))
    return hasher.hexdigest() == hashed_password_hex

def generate_hmac(message: bytes, key: bytes) -> str:
    """Generate HMAC for message integrity (optional enhancement)."""
    import hmac
    return hmac.new(key, message, hashlib.sha256).hexdigest()
