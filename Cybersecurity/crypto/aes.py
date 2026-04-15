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
    """
    Generate a random 256-bit AES session key.
    
    Returns:
        bytes: 32-byte random key suitable for AES-256.
    """
    return get_random_bytes(32)


def encrypt_aes(plaintext: str, key: bytes) -> Tuple[str, str]:
    """
    Encrypt plaintext using AES-256-CBC mode.
    
    Uses CBC mode with PKCS7 padding for security and compatibility.
    Both ciphertext and IV are Base64 encoded for safe transmission.
    
    Args:
        plaintext (str): Message to encrypt.
        key (bytes): 256-bit AES key (32 bytes).
    
    Returns:
        Tuple[str, str]: (base64_ciphertext, base64_iv)
    
    Raises:
        Exception: If encryption fails or invalid key size.
    """
    # Generate random IV for this encryption
    iv = get_random_bytes(16)
    
    # Create cipher in CBC mode
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Pad plaintext to block size and encrypt
    padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    
    # Return Base64 encoded ciphertext and IV
    return (
        base64.b64encode(ciphertext).decode('utf-8'),
        base64.b64encode(iv).decode('utf-8')
    )


def decrypt_aes(ciphertext_b64: str, key: bytes, iv_b64: str) -> str:
    """
    Decrypt AES-256-CBC ciphertext.
    
    Args:
        ciphertext_b64 (str): Base64-encoded ciphertext.
        key (bytes): 256-bit AES key (32 bytes) used for encryption.
        iv_b64 (str): Base64-encoded IV from encryption.
    
    Returns:
        str: Decrypted plaintext message.
    
    Raises:
        Exception: If decryption fails, invalid key, or corrupted data.
    """
    # Decode Base64
    ciphertext = base64.b64decode(ciphertext_b64)
    iv = base64.b64decode(iv_b64)
    
    # Decrypt
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(ciphertext)
    
    # Remove padding and decode to string
    plaintext = unpad(decrypted_padded, AES.block_size).decode('utf-8')
    
    return plaintext
