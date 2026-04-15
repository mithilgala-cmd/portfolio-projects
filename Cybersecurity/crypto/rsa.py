# crypto/rsa.py
"""
RSA encryption module for key exchange.
Provides RSA-2048 asymmetric encryption with OAEP padding.
"""

import base64
from typing import Tuple
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP


def generate_rsa_key_pair() -> Tuple[bytes, bytes]:
    """
    Generate 2048-bit RSA key pair in PEM format.
    
    This is used for asymmetric key exchange - each client generates
    a public/private key pair and shares the public key with the server.
    The public key is used to encrypt AES session keys for secure delivery.
    
    Returns:
        Tuple[bytes, bytes]: (private_key_pem, public_key_pem)
    
    Note:
        - Private key should be kept secret and never transmitted
        - Public key is sent to server during authentication
        - RSA-2048 provides ~112 bits of symmetric strength
    """
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key


def encrypt_with_public_key(message: bytes, public_key_pem: bytes) -> str:
    """
    Encrypt message (e.g., AES session key) with recipient's RSA public key.
    
    Uses PKCS1-OAEP padding for semantic security. This ensures that
    encrypting the same plaintext multiple times produces different
    ciphertexts due to random padding.
    
    Args:
        message (bytes): Data to encrypt (typically an AES session key).
        public_key_pem (bytes): Recipient's RSA public key in PEM format.
    
    Returns:
        str: Base64-encoded ciphertext.
    
    Raises:
        Exception: If message is too large for RSA-2048 or encryption fails.
    
    Note:
        Message length is limited to ~190 bytes for RSA-2048 with OAEP.
        This is typically used for encrypting 32-byte AES keys.
    """
    recipient_key = RSA.import_key(public_key_pem)
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_data = cipher_rsa.encrypt(message)
    return base64.b64encode(enc_data).decode('utf-8')


def decrypt_with_private_key(encrypted_data_b64: str, private_key_pem: bytes) -> bytes:
    """
    Decrypt message with your own RSA private key.
    
    Used to recover AES session keys encrypted with your public key.
    Only the holder of the private key can perform this decryption.
    
    Args:
        encrypted_data_b64 (str): Base64-encoded ciphertext from encryption.
        private_key_pem (bytes): Your RSA private key in PEM format.
    
    Returns:
        bytes: Decrypted plaintext (typically an AES session key).
    
    Raises:
        Exception: If decryption fails or data is corrupted.
    
    Security:
        - Private key must never be shared or transmitted
        - If private key is compromised, all encrypted data can be decrypted
        - This function should only be called locally on the client
    """
    enc_data = base64.b64decode(encrypted_data_b64)
    private_key = RSA.import_key(private_key_pem)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    dec_data = cipher_rsa.decrypt(enc_data)
    return dec_data
