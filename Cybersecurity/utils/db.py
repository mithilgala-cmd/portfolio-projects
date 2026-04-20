"""
Production-ready database module for persistent credential storage.

Uses SQLite for user credentials with proper schema and migration support.
Supports both production (persistent) and development (in-memory) modes.
"""

import sqlite3
import os
import sys
import logging
from typing import Dict, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

# Database configuration
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'secure_chat.db')
PRODUCTION_MODE = os.environ.get('SECURE_CHAT_MODE', 'production').lower() == 'production'


class Database:
    """SQLite database handler for user credentials."""
    
    def __init__(self, db_path: str = DB_PATH, production: bool = PRODUCTION_MODE):
        """
        Initialize database connection.
        
        Args:
            db_path: Path to SQLite database file
            production: If True, use persistent storage; if False, use in-memory
        """
        self.production = production
        self.db_path = db_path if production else ':memory:'
        self.conn = None
        self.init_db()
    
    def get_connection(self) -> sqlite3.Connection:
        """Get or create database connection."""
        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
        return self.conn
    
    def close(self) -> None:
        """Close database connection."""
        if self.conn:
            self.conn.close()
            self.conn = None
    
    def init_db(self) -> None:
        """Initialize database schema."""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY,
                password_hash TEXT NOT NULL,
                salt TEXT NOT NULL,
                failed_attempts INTEGER DEFAULT 0,
                last_failed_attempt REAL DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Create index on username for faster lookups
        cursor.execute('''
            CREATE INDEX IF NOT EXISTS idx_username ON users(username)
        ''')
        
        conn.commit()
        logger.info(f"Database initialized: {'SQLite file' if self.production else 'In-memory'}")
    
    def user_exists(self, username: str) -> bool:
        """Check if user exists in database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT 1 FROM users WHERE username = ?', (username,))
        return cursor.fetchone() is not None
    
    def create_user(self, username: str, password_hash: str, salt: str) -> bool:
        """Create new user in database."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO users (username, password_hash, salt, failed_attempts, last_failed_attempt)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, password_hash, salt, 0, 0))
            conn.commit()
            logger.info(f"User '{username}' created in database")
            return True
        except sqlite3.IntegrityError:
            logger.warning(f"User '{username}' already exists")
            return False
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return False
    
    def get_user(self, username: str) -> Optional[Dict]:
        """Get user from database."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT username, password_hash, salt, failed_attempts, last_failed_attempt
            FROM users WHERE username = ?
        ''', (username,))
        row = cursor.fetchone()
        
        if row:
            return {
                'username': row['username'],
                'hash': row['password_hash'],
                'salt': row['salt'],
                'attempts': row['failed_attempts'],
                'last_attempt': row['last_failed_attempt']
            }
        return None
    
    def update_failed_attempts(self, username: str, attempts: int, last_attempt: float) -> bool:
        """Update failed login attempts."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users 
                SET failed_attempts = ?, last_failed_attempt = ?, updated_at = CURRENT_TIMESTAMP
                WHERE username = ?
            ''', (attempts, last_attempt, username))
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error updating failed attempts: {e}")
            return False
    
    def reset_failed_attempts(self, username: str) -> bool:
        """Reset failed login attempts after successful login."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users 
                SET failed_attempts = 0, last_failed_attempt = 0, updated_at = CURRENT_TIMESTAMP
                WHERE username = ?
            ''', (username,))
            conn.commit()
            return True
        except Exception as e:
            logger.error(f"Error resetting failed attempts: {e}")
            return False
    
    def get_all_users(self) -> list:
        """Get all users (for admin/testing purposes)."""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT username, created_at, updated_at FROM users')
        return [dict(row) for row in cursor.fetchall()]
    
    def delete_user(self, username: str) -> bool:
        """Delete user from database."""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute('DELETE FROM users WHERE username = ?', (username,))
            conn.commit()
            logger.info(f"User '{username}' deleted from database")
            return True
        except Exception as e:
            logger.error(f"Error deleting user: {e}")
            return False


# Global database instance
_db_instance: Optional[Database] = None


def get_db() -> Database:
    """Get or create global database instance."""
    global _db_instance
    if _db_instance is None:
        _db_instance = Database()
    return _db_instance


def init_db_instance(db_path: str = DB_PATH, production: bool = PRODUCTION_MODE) -> Database:
    """Initialize and return database instance."""
    global _db_instance
    _db_instance = Database(db_path, production)
    return _db_instance
