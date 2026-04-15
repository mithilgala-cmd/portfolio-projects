# crypto/rsa.py
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

def generate_rsa_key_pair() -> tuple[bytes, bytes]:
    """Generate 2048-bit RSA key pair (private_key, public_key) in PEM format."""
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    return private_key, public_key

def encrypt_with_public_key(message: bytes, public_key_pem: bytes) -> str:
    """Encrypt message (e.g., AES session key) with receiver's RSA public key."""
    recipient_key = RSA.import_key(public_key_pem)
    cipher_rsa = PKCS1_OAEP.new(recipient_key)
    enc_data = cipher_rsa.encrypt(message)
    return base64.b64encode(enc_data).decode('utf-8')

def decrypt_with_private_key(encrypted_data_b64: str, private_key_pem: bytes) -> bytes:
    """Decrypt message with your own RSA private key."""
    enc_data = base64.b64decode(encrypted_data_b64)
    private_key = RSA.import_key(private_key_pem)
    cipher_rsa = PKCS1_OAEP.new(private_key)
    dec_data = cipher_rsa.decrypt(enc_data)
    return dec_data
