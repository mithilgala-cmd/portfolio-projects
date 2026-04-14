# crypto/aes.py
import base64
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def generate_aes_key() -> bytes:
    """Generate a random 256-bit AES session key."""
    return get_random_bytes(32)

def encrypt_aes(plaintext: str, key: bytes) -> tuple[str, str]:
    """
    Encrypt plaintext using AES-CBC mode.
    Returns Base64 encoded (ciphertext, iv).
    """
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_data = pad(plaintext.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_data)
    
    return base64.b64encode(ciphertext).decode('utf-8'), base64.b64encode(iv).decode('utf-8')

def decrypt_aes(ciphertext_b64: str, key: bytes, iv_b64: str) -> str:
    """
    Decrypt AES-CBC ciphertext.
    Requires Base64 encoded ciphertext and iv.
    """
    ciphertext = base64.b64decode(ciphertext_b64)
    iv = base64.b64decode(iv_b64)
    
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_padded = cipher.decrypt(ciphertext)
    plaintext = unpad(decrypted_padded, AES.block_size).decode('utf-8')
    
    return plaintext
