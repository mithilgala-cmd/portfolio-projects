# utils/config.py
"""
Central configuration module for the Secure Chat Application.

Defines all configuration constants including network settings,
cryptographic parameters, and security constraints.
"""

# Network Configuration
"""Server binding address (localhost for development)."""
HOST = '127.0.0.1'

"""Server listening port."""
PORT = 65432

"""Socket buffer size for receiving messages (bytes)."""
BUFFER_SIZE = 4096

"""Socket timeout for recv operations (seconds)."""
TIMEOUT = 60.0

# Cryptographic Configuration

"""Salt size for password hashing (bytes). Must be at least 16."""
SALT_SIZE = 16

"""Number of iterations for PBKDF2. Higher = more secure but slower.
Recommended: 100,000+ for production. Current: 100,000 iterations."""
HASH_ITERATIONS = 100000

"""RSA key size for asymmetric encryption (bits). 
Common: 2048 (minimum), 4096 (recommended for long-term security)."""
KEY_SIZE_RSA = 2048

# Authentication & Rate Limiting

"""Maximum failed login attempts before account lockout."""
MAX_AUTH_ATTEMPTS = 5

"""Lockout duration after max failed attempts (seconds)."""
LOCKOUT_DURATION_SECONDS = 300

# Input Validation

"""Minimum username length (characters)."""
MIN_USERNAME_LENGTH = 3

"""Maximum username length (characters)."""
MAX_USERNAME_LENGTH = 20

"""Minimum password length (characters)."""
MIN_PASSWORD_LENGTH = 8

"""Maximum password length (characters)."""
MAX_PASSWORD_LENGTH = 128
