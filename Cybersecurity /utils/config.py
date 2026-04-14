# utils/config.py
"""
Configuration settings for the Secure Chat Application.
"""

HOST = '127.0.0.1'
PORT = 65432
BUFFER_SIZE = 4096
TIMEOUT = 60.0

# Security Configuration
SALT_SIZE = 16
HASH_ITERATIONS = 100000
KEY_SIZE_RSA = 2048
