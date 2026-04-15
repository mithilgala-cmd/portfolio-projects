"""
Unit tests for cryptographic modules (AES and RSA).
Tests encryption/decryption correctness and edge cases.
"""

import unittest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crypto.aes import generate_aes_key, encrypt_aes, decrypt_aes
from crypto.rsa import generate_rsa_key_pair, encrypt_with_public_key, decrypt_with_private_key


class TestAESEncryption(unittest.TestCase):
    """Test suite for AES encryption module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.key = generate_aes_key()
        self.test_messages = [
            "Hello, World!",
            "Top secret message",
            "A" * 1000,  # Long message
            "Special chars: @#$%^&*()",
            "Emoji test: 🔐🔒🔑",
            "",  # Empty string (edge case)
        ]
    
    def test_aes_key_generation(self):
        """Test AES key generation produces correct size."""
        key = generate_aes_key()
        self.assertEqual(len(key), 32)  # 256 bits = 32 bytes
        
        # Keys should be different each time
        key2 = generate_aes_key()
        self.assertNotEqual(key, key2)
    
    def test_encrypt_decrypt_basic(self):
        """Test basic encrypt/decrypt cycle."""
        plaintext = "Test message"
        ciphertext_b64, iv_b64 = encrypt_aes(plaintext, self.key)
        decrypted = decrypt_aes(ciphertext_b64, self.key, iv_b64)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_encrypt_decrypt_all_messages(self):
        """Test encrypt/decrypt for various message types."""
        for message in self.test_messages:
            with self.subTest(message=message[:20]):
                ciphertext_b64, iv_b64 = encrypt_aes(message, self.key)
                decrypted = decrypt_aes(ciphertext_b64, self.key, iv_b64)
                self.assertEqual(message, decrypted)
    
    def test_encryption_produces_different_ciphertexts(self):
        """Test that same plaintext produces different ciphertext (due to random IV)."""
        plaintext = "Same message"
        ct1, iv1 = encrypt_aes(plaintext, self.key)
        ct2, iv2 = encrypt_aes(plaintext, self.key)
        
        # Ciphertexts should be different (different IVs)
        self.assertNotEqual(ct1, ct2)
        self.assertNotEqual(iv1, iv2)
        
        # But both should decrypt to same plaintext
        self.assertEqual(decrypt_aes(ct1, self.key, iv1), plaintext)
        self.assertEqual(decrypt_aes(ct2, self.key, iv2), plaintext)
    
    def test_wrong_key_decryption_fails(self):
        """Test that using wrong key for decryption fails gracefully."""
        plaintext = "Secret"
        ciphertext_b64, iv_b64 = encrypt_aes(plaintext, self.key)
        
        wrong_key = generate_aes_key()
        with self.assertRaises(Exception):
            decrypt_aes(ciphertext_b64, wrong_key, iv_b64)
    
    def test_base64_encoding(self):
        """Test that ciphertext and IV are properly Base64 encoded."""
        plaintext = "Test"
        ciphertext_b64, iv_b64 = encrypt_aes(plaintext, self.key)
        
        # Should be valid Base64 strings
        import base64
        try:
            base64.b64decode(ciphertext_b64)
            base64.b64decode(iv_b64)
        except Exception as e:
            self.fail(f"Invalid Base64 encoding: {e}")


class TestRSAEncryption(unittest.TestCase):
    """Test suite for RSA encryption module."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.private_key, self.public_key = generate_rsa_key_pair()
        self.test_data = [
            b"Hello",
            b"Secret key",
            b"A" * 32,  # Typical AES key size
        ]
    
    def test_rsa_key_pair_generation(self):
        """Test RSA key pair generation."""
        priv, pub = generate_rsa_key_pair()
        
        # Keys should be bytes
        self.assertIsInstance(priv, bytes)
        self.assertIsInstance(pub, bytes)
        
        # Keys should start with PEM header
        self.assertIn(b"BEGIN", priv)
        self.assertIn(b"BEGIN", pub)
        
        # Private key should be longer than public key
        self.assertGreater(len(priv), len(pub))
    
    def test_encrypt_decrypt_basic(self):
        """Test basic RSA encrypt/decrypt cycle."""
        plaintext = b"Test data"
        encrypted_b64 = encrypt_with_public_key(plaintext, self.public_key)
        decrypted = decrypt_with_private_key(encrypted_b64, self.private_key)
        
        self.assertEqual(plaintext, decrypted)
    
    def test_encrypt_decrypt_all_data(self):
        """Test RSA encrypt/decrypt for various data sizes."""
        for data in self.test_data:
            with self.subTest(data_len=len(data)):
                encrypted_b64 = encrypt_with_public_key(data, self.public_key)
                decrypted = decrypt_with_private_key(encrypted_b64, self.private_key)
                self.assertEqual(data, decrypted)
    
    def test_encryption_produces_different_ciphertexts(self):
        """Test that same data produces different ciphertext (OAEP randomization)."""
        data = b"Same data"
        ct1 = encrypt_with_public_key(data, self.public_key)
        ct2 = encrypt_with_public_key(data, self.public_key)
        
        # Ciphertexts should be different (OAEP padding)
        self.assertNotEqual(ct1, ct2)
        
        # But both should decrypt to same data
        self.assertEqual(decrypt_with_private_key(ct1, self.private_key), data)
        self.assertEqual(decrypt_with_private_key(ct2, self.private_key), data)
    
    def test_wrong_key_decryption_fails(self):
        """Test that using wrong key for decryption fails."""
        data = b"Secret"
        encrypted_b64 = encrypt_with_public_key(data, self.public_key)
        
        # Generate different key pair
        _, pub2 = generate_rsa_key_pair()
        priv2, _ = generate_rsa_key_pair()
        
        # Encrypting with pub1 but decrypting with priv2 should fail
        with self.assertRaises(Exception):
            decrypt_with_private_key(encrypted_b64, priv2)
    
    def test_cross_pair_encryption_fails(self):
        """Test that data encrypted with one key pair can't be decrypted with another."""
        data = b"Test"
        encrypted = encrypt_with_public_key(data, self.public_key)
        
        # Generate different key pair
        priv2, _ = generate_rsa_key_pair()
        
        # Should fail to decrypt
        with self.assertRaises(Exception):
            decrypt_with_private_key(encrypted, priv2)
    
    def test_base64_encoding(self):
        """Test that encrypted data is properly Base64 encoded."""
        data = b"Test"
        encrypted_b64 = encrypt_with_public_key(data, self.public_key)
        
        # Should be valid Base64 string
        import base64
        try:
            base64.b64decode(encrypted_b64)
        except Exception as e:
            self.fail(f"Invalid Base64 encoding: {e}")


class TestE2EEncryption(unittest.TestCase):
    """End-to-end encryption tests combining AES and RSA."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Generate two key pairs (sender and receiver)
        self.sender_priv, self.sender_pub = generate_rsa_key_pair()
        self.receiver_priv, self.receiver_pub = generate_rsa_key_pair()
    
    def test_e2e_message_encryption(self):
        """Test complete E2E encryption flow: message -> AES encrypt -> RSA encrypt."""
        message = "This is a secret message!"
        
        # Step 1: Generate AES session key
        session_key = generate_aes_key()
        
        # Step 2: Encrypt message with AES
        ct_msg, iv = encrypt_aes(message, session_key)
        
        # Step 3: Encrypt AES key with receiver's RSA public key
        ct_key = encrypt_with_public_key(session_key, self.receiver_pub)
        
        # --- Transmission happens here ---
        
        # Step 4: Receiver decrypts AES key with their private key
        decrypted_key = decrypt_with_private_key(ct_key, self.receiver_priv)
        
        # Step 5: Receiver decrypts message with AES key
        decrypted_msg = decrypt_aes(ct_msg, decrypted_key, iv)
        
        self.assertEqual(message, decrypted_msg)
    
    def test_e2e_prevents_server_decryption(self):
        """Test that server with only public key cannot decrypt message."""
        message = "Secret"
        session_key = generate_aes_key()
        
        # E2E encryption
        ct_msg, iv = encrypt_aes(message, session_key)
        ct_key = encrypt_with_public_key(session_key, self.receiver_pub)
        
        # Server has only receiver's public key - cannot decrypt
        with self.assertRaises(Exception):
            # Can't decrypt session key without private key
            decrypt_with_private_key(ct_key, self.receiver_pub)


if __name__ == '__main__':
    unittest.main()
