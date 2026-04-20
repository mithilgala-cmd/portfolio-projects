"""
Unit tests for authentication module.
Tests user registration, login, rate limiting, and input validation.
"""

import unittest
import sys
import os
import time

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from auth import auth
from crypto.hash import hash_password, verify_password
from utils.db import init_db_instance

# Initialize in-memory database for testing
def setup_test_db():
    """Initialize in-memory database for testing."""
    from utils import db as db_module
    if db_module._db_instance is not None:
        db_module._db_instance.close()
    return init_db_instance(db_path=':memory:', production=False)


class TestPasswordHashing(unittest.TestCase):
    """Test suite for password hashing functions."""
    
    def test_hash_password_generates_different_salts(self):
        """Test that hashing produces different salts each time."""
        password = "TestPassword123"
        
        hash1, salt1 = hash_password(password)
        hash2, salt2 = hash_password(password)
        
        # Salts should be different
        self.assertNotEqual(salt1, salt2)
        # Hashes should be different (due to different salts)
        self.assertNotEqual(hash1, hash2)
    
    def test_verify_correct_password(self):
        """Test verifying correct password."""
        password = "MySecretPassword"
        
        hashed, salt = hash_password(password)
        result = verify_password(password, hashed, salt)
        
        self.assertTrue(result)
    
    def test_verify_incorrect_password(self):
        """Test verifying incorrect password."""
        password = "CorrectPassword"
        wrong_password = "WrongPassword"
        
        hashed, salt = hash_password(password)
        result = verify_password(wrong_password, hashed, salt)
        
        self.assertFalse(result)
    
    def test_verify_password_case_sensitive(self):
        """Test that password verification is case-sensitive."""
        password = "TestPassword"
        
        hashed, salt = hash_password(password)
        result = verify_password("testpassword", hashed, salt)
        
        self.assertFalse(result)
    
    def test_hash_consistency(self):
        """Test that same password with same salt produces same hash."""
        password = "ConsistentPassword"
        from crypto.hash import generate_salt
        salt = generate_salt()
        
        hash1, salt1 = hash_password(password, salt)
        hash2, salt2 = hash_password(password, salt)
        
        self.assertEqual(hash1, hash2)
        self.assertEqual(salt1, salt2)


class TestInputValidation(unittest.TestCase):
    """Test suite for input validation functions."""
    
    def test_valid_usernames(self):
        """Test acceptance of valid usernames."""
        valid_usernames = [
            "alice",
            "bob123",
            "user_name",
            "test_user_123",
            "a" * 20,  # Max length
            "abc",  # Min length
        ]
        
        for username in valid_usernames:
            with self.subTest(username=username):
                self.assertTrue(auth.is_valid_username(username))
    
    def test_invalid_usernames(self):
        """Test rejection of invalid usernames."""
        invalid_usernames = [
            "",  # Empty
            "ab",  # Too short
            "a" * 21,  # Too long
            "user-name",  # Invalid character
            "user name",  # Contains space
            "user@domain",  # Invalid character
            "123!?#",  # Invalid characters
        ]
        
        for username in invalid_usernames:
            with self.subTest(username=username):
                self.assertFalse(auth.is_valid_username(username))
    
    def test_valid_passwords(self):
        """Test acceptance of valid passwords."""
        valid_passwords = [
            "password123",
            "MyP@ssw0rd!",
            "a" * 8,  # Min length
            "a" * 128,  # Max length
            "VeryLongPasswordWithSpecialChars!@#$%^&*()",
        ]
        
        for password in valid_passwords:
            with self.subTest(password_len=len(password)):
                self.assertTrue(auth.is_valid_password(password))
    
    def test_invalid_passwords(self):
        """Test rejection of invalid passwords."""
        invalid_passwords = [
            "",  # Empty
            "short",  # Too short (< 8)
            "a" * 129,  # Too long (> 128)
            None,  # None type
        ]
        
        for password in invalid_passwords:
            with self.subTest(password=str(password)):
                self.assertFalse(auth.is_valid_password(password))


class TestUserRegistration(unittest.TestCase):
    """Test suite for user registration."""
    
    def setUp(self):
        """Clear user store and reset database before each test."""
        auth.USER_STORE.clear()
        # Reinitialize database in memory for each test
        from utils import db as db_module
        db_module._db_instance = setup_test_db()
    
    def test_register_new_user(self):
        """Test successful registration of new user."""
        success, message = auth.register_user("alice", "password123")
        
        self.assertTrue(success)
        self.assertEqual(message, "Success")
        self.assertIn("alice", auth.USER_STORE)
    
    def test_register_duplicate_user(self):
        """Test that duplicate registration fails."""
        auth.register_user("alice", "password123")
        success, message = auth.register_user("alice", "different_password")
        
        self.assertFalse(success)
    
    def test_register_invalid_username(self):
        """Test registration with invalid username."""
        success, message = auth.register_user("ab", "password123")
        
        self.assertFalse(success)
        self.assertNotIn("ab", auth.USER_STORE)
    
    def test_register_invalid_password(self):
        """Test registration with invalid password."""
        success, message = auth.register_user("alice", "short")
        
        self.assertFalse(success)
        self.assertNotIn("alice", auth.USER_STORE)
    
    def test_register_generic_error_messages(self):
        """Test that error messages are generic (don't leak info)."""
        # First registration succeeds
        auth.register_user("alice", "password123")
        
        # Duplicate registration should give generic error
        success, message = auth.register_user("alice", "password123")
        
        self.assertFalse(success)
        # Should not say "User already exists"
        self.assertNotIn("already exists", message)


class TestAuthentication(unittest.TestCase):
    """Test suite for user authentication."""
    
    def setUp(self):
        """Clear user store and set up test user."""
        auth.USER_STORE.clear()
        from utils import db as db_module
        db_module._db_instance = setup_test_db()
        auth.register_user("alice", "password123")
    
    def test_login_correct_credentials(self):
        """Test successful login with correct credentials."""
        success, message = auth.authenticate_user("alice", "password123")
        
        self.assertTrue(success)
        self.assertEqual(message, "Success")
    
    def test_login_incorrect_password(self):
        """Test failed login with incorrect password."""
        success, message = auth.authenticate_user("alice", "wrongpassword")
        
        self.assertFalse(success)
    
    def test_login_nonexistent_user(self):
        """Test failed login with non-existent user."""
        success, message = auth.authenticate_user("bob", "password123")
        
        self.assertFalse(success)
    
    def test_login_generic_error_messages(self):
        """Test that error messages are generic."""
        success, message = auth.authenticate_user("alice", "wrongpassword")
        
        self.assertFalse(success)
        # Should not leak information
        self.assertNotIn("password", message.lower())


class TestRateLimiting(unittest.TestCase):
    """Test suite for rate limiting and account lockout."""
    
    def setUp(self):
        """Clear user store and set up test user."""
        auth.USER_STORE.clear()
        from utils import db as db_module
        db_module._db_instance = setup_test_db()
        auth.register_user("alice", "correct_password")
        
        # Temporarily reduce for testing
        self.original_max = auth.MAX_ATTEMPTS
        self.original_lockout = auth.LOCKOUT_DURATION
        auth.MAX_ATTEMPTS = 3
        auth.LOCKOUT_DURATION = 2  # 2 seconds for testing
    
    def tearDown(self):
        """Restore original settings."""
        auth.MAX_ATTEMPTS = self.original_max
        auth.LOCKOUT_DURATION = self.original_lockout
    
    def test_failed_login_increments_counter(self):
        """Test that failed logins increment attempt counter."""
        from utils.db import get_db
        db = get_db()
        initial_attempts = db.get_user("alice").get("attempts", 0)
        
        auth.authenticate_user("alice", "wrong_password")
        
        self.assertEqual(db.get_user("alice").get("attempts", 0), initial_attempts + 1)
    
    def test_successful_login_resets_counter(self):
        """Test that successful login resets attempt counter."""
        # Make some failed attempts
        auth.authenticate_user("alice", "wrong_password")
        auth.authenticate_user("alice", "wrong_password")
        
        # Successful login should reset
        success, _ = auth.authenticate_user("alice", "correct_password")
        
        from utils.db import get_db
        db = get_db()
        self.assertTrue(success)
        self.assertEqual(db.get_user("alice")["attempts"], 0)
    
    def test_account_lockout_after_max_attempts(self):
        """Test account lockout after max failed attempts."""
        # Make max failed attempts
        for _ in range(auth.MAX_ATTEMPTS):
            auth.authenticate_user("alice", "wrong_password")
        
        # Account should be locked
        self.assertTrue(auth.is_account_locked("alice"))
        
        # Even with correct password, should fail
        success, _ = auth.authenticate_user("alice", "correct_password")
        self.assertFalse(success)
    
    def test_lockout_timeout_expires(self):
        """Test that lockout expires after lockout duration."""
        # Lock the account
        for _ in range(auth.MAX_ATTEMPTS):
            auth.authenticate_user("alice", "wrong_password")
        
        self.assertTrue(auth.is_account_locked("alice"))
        
        # Wait for lockout to expire
        time.sleep(auth.LOCKOUT_DURATION + 0.1)
        
        # Account should no longer be locked
        self.assertFalse(auth.is_account_locked("alice"))
        
        # Should be able to login with correct password
        success, _ = auth.authenticate_user("alice", "correct_password")
        self.assertTrue(success)
    
    def test_generic_error_during_lockout(self):
        """Test that locked account returns generic error."""
        # Lock the account
        for _ in range(auth.MAX_ATTEMPTS):
            auth.authenticate_user("alice", "wrong_password")
        
        # Try to login
        success, message = auth.authenticate_user("alice", "correct_password")
        
        self.assertFalse(success)
        # Should not mention account lockout
        self.assertNotIn("lock", message.lower())


class TestConcurrentSecurity(unittest.TestCase):
    """Test suite for security against concurrent/timing attacks."""
    
    def setUp(self):
        """Clear user store and reset database."""
        auth.USER_STORE.clear()
        from utils import db as db_module
        db_module._db_instance = setup_test_db()
    
    def test_generic_error_prevents_enumeration(self):
        """Test that generic error messages prevent user enumeration attacks.
        
        Both non-existent users and existing users with wrong passwords
        return the same generic error message.
        """
        auth.register_user("alice", "password123")
        
        # Non-existent user
        success1, msg1 = auth.authenticate_user("bob", "password")
        
        # Existing user, wrong password
        success2, msg2 = auth.authenticate_user("alice", "wrongpass")
        
        # Both should fail
        self.assertFalse(success1)
        self.assertFalse(success2)
        
        # Both should return the same generic error message
        self.assertEqual(msg1, msg2)
        
        # Message should not leak information
        self.assertEqual(msg1, "Authentication failed.")


if __name__ == '__main__':
    unittest.main()
