# crypto/aes.py
"""
AES encryption module for message encryption.
Provides AES-256-CBC encryption with PKCS7 padding.
"""

import base64
from typing import Tuple
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def generate_aes_key() -> bytes:
    """Generate a random 256-bit AES session key."""
    return get_random_bytes(32)


def encrypt_aes(plaintext: str, key: bytes) -> Tuple[str, str]:
    """Encrypt plaintext using AES-256-CBC with PKCS7 padding."""
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    
    return (
        base64.b64encode(ciphertext).decode('utf-8'),
        base64.b64encode(iv).decode('utf-8')
    )


def decrypt_aes(ciphertext_b64: str, key: bytes, iv_b64: str) -> str:
    """Decrypt AES-256-CBC ciphertext."""
    ciphertext = base64.b64decode(ciphertext_b64)
    iv = base64.b64decode(iv_b64)
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(ciphertext)
    
    return unpad(decrypted_padded, AES.block_size).decode('utf-8')
