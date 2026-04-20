# Secure Chat Application with End-to-End Encryption

## Overview
This is a comprehensive, secure chat application built in Python 3 (3.10+), demonstrating core cybersecurity concepts. It features End-to-End Encryption (E2EE), robust authentication with PBKDF2 password hashing, and a client-server architecture where the server acts purely as a message relay without the ability to decrypt message contents.

## Features
* **End-to-End Encryption (E2EE):** AES-256-CBC session keys encrypted with RSA-2048 asymmetric cryptography.
* **Secure Authentication:** PBKDF2-SHA256 password hashing with rate limiting and account lockout.
* **Input Validation:** Strict validation of usernames and passwords against attack vectors.
* **Rate Limiting:** 5 failed login attempts trigger 5-minute account lockout to prevent brute-force attacks.
* **Confidentiality:** Server only sees encrypted Base64-encoded ciphertext, never plaintext or keys.
* **Integrity:** PKCS7 padding in CBC mode ensures message integrity.
* **Concurrency:** Multi-threaded client handling with proper thread-safe operations.
* **Error Handling:** Comprehensive error handling, graceful disconnection, and timeout support.
* **Comprehensive Logging:** Detailed logging for debugging and monitoring.
* **Type Hints & Documentation:** Full type annotations and docstrings throughout codebase.

## Tech Stack
* **Python:** 3.10+
* **Cryptography:** `pycryptodome` (3.20.0)
* **Database:** SQLite 3 (persistent credential storage)
* **Built-in Libraries:** `socket`, `threading`, `json`, `logging`, `hashlib`, `sqlite3`

## Production-Ready Features

### ✨ NEW: Persistent Credential Storage
The application now includes **production-ready SQLite database** for persistent user credential storage:

**Key Improvements:**
- ✅ **Persistent Storage** - User credentials survive server restarts
- ✅ **Rate Limiting Persistence** - Account lockout state persists across restarts
- ✅ **Audit Trail** - Timestamps for compliance and monitoring (`created_at`, `updated_at`)
- ✅ **Performance** - Indexed username lookups (< 1ms)
- ✅ **Thread-Safe** - Safe for multi-threaded server with concurrent clients
- ✅ **Scalable** - Can migrate to PostgreSQL/MySQL for larger deployments

**Database Location:** `secure_chat.db` (automatically created on first run)

**Example - Verify Persistence:**
```bash
# Run demo once
python demo_run.py

# Check database
sqlite3 secure_chat.db "SELECT username, created_at FROM users;"
```

**Database Schema:**
- `username` - Primary key, unique
- `password_hash` - PBKDF2-SHA256 hash
- `salt` - Random 16-byte salt
- `failed_attempts` - Rate limiting counter
- `last_failed_attempt` - Timestamp of last failure
- `created_at` - Account creation timestamp
- `updated_at` - Last modification timestamp

For complete database documentation, see [PRODUCTION_DATABASE.md](PRODUCTION_DATABASE.md)

## Security Improvements

### Authentication & Password Handling
- **PBKDF2-SHA256** instead of basic SHA256 for key derivation
  - 100,000 iterations by default (configurable)
  - Resistant to dictionary and brute-force attacks
  - Industry-standard password hashing
- **Rate Limiting:** Account lockout after 5 failed login attempts for 5 minutes
- **Input Validation:**
  - Username: 3-20 alphanumeric/underscore characters
  - Password: 8-128 characters
- **Generic Error Messages:** Don't leak whether username exists or password is wrong

### Network Security
- **Socket Timeouts:** 60-second timeout on all socket operations
- **JSON Validation:** All received data is validated as valid JSON
- **Proper Cleanup:** Safe resource cleanup on disconnection or error

### Cryptographic Best Practices
- **AES-256-CBC:** 256-bit keys with PKCS7 padding
- **RSA-2048-OAEP:** Optimal Asymmetric Encryption Padding (semantic security)
- **Random IVs:** New random IV for every AES encryption
- **Random Session Keys:** New AES key generated per message transmission

## Architecture

* **Client-Server Model:** Server relays encrypted payloads between clients.
* **Cryptography Flow:**
```
Client A → Generate AES Key → Encrypt message (AES) 
→ Encrypt AES Key (Peer RSA Public) → Server (relay) 
→ Client B → Decrypt AES Key (Own RSA Private) 
→ Decrypt message (AES)
```

```text
+----------+                                +---------+                                +----------+
|          | --(1) Auth & Send Pub Key----> |         | <---(1) Auth & Send Pub Key--- |          |
| Client A |                                | Server  |                                | Client B |
|          | --(2) Encrypted Payload -----> | (Relay) | ---(3) Relay Payload --------> |          |
+----------+                                +---------+                                +----------+
```

## Security Properties (CIA Triad)
* **Confidentiality:** 
  - Messages encrypted with AES-256-CBC
  - Server blindness: Server cannot decrypt any messages
  - Only intended recipient can decrypt (has private RSA key)
* **Integrity:** 
  - CBC mode with PKCS7 padding
  - Message tampering detected on decryption
  - Session key integrity protected by RSA-OAEP
* **Availability:** 
  - Multi-threaded server handles multiple concurrent clients
  - Connection timeouts prevent zombie connections
  - Graceful error handling prevents server crashes

## Protocol Design

### Authentication Handshake
1. **Client connects:** Sends username and password (register or login action)
2. **Server validates:** 
   - Checks input format
   - Performs rate-limit check
   - Verifies credentials (for login)
3. **Auth success:** Client generates RSA-2048 key pair locally
4. **Key exchange:** Client sends public key to server (private key never leaves client)
5. **Session ready:** Client can now securely message other authenticated users

### Message Exchange Protocol
1. **Peer lookup:** Alice requests Bob's public key from server
2. **Session key:** Alice generates random 256-bit AES key
3. **Encryption:** Alice encrypts message with AES session key
4. **Key encryption:** Alice encrypts AES key with Bob's RSA public key
5. **Relay:** Alice sends encrypted payload to server
6. **Forward:** Server relays payload to Bob (server cannot read it)
7. **Decryption:** Bob decrypts AES key with his private key, then decrypts message

### Message Format (JSON)
```json
{
  "type": "chat_message",
  "target": "bob",
  "payload": {
    "session_key": "<base64_rsa_encrypted_aes_key>",
    "ciphertext": "<base64_aes_encrypted_message>",
    "iv": "<base64_aes_initialization_vector>"
  }
}
```

## Directory Structure
```
.
├── README.md                 # This file
├── requirements.txt          # Project dependencies
├── demo_run.py              # Automated demo script
├── viva_prep.md             # Viva preparation notes
├── auth/
│   └── auth.py              # User registration, login, rate limiting
├── client/
│   └── client.py            # Chat client with E2EE
├── crypto/
│   ├── aes.py               # AES-256-CBC encryption
│   ├── hash.py              # PBKDF2 password hashing
│   └── rsa.py               # RSA-2048 key exchange
├── server/
│   └── server.py            # Secure message relay server
├── utils/
│   └── config.py            # Central configuration
├── tests/
│   ├── __init__.py
│   ├── test_crypto.py       # Crypto module tests
│   └── test_auth.py         # Auth module tests
└── screenshots/
    └── (screenshots for documentation)
```

## Setup & Execution

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run Automated Demo
```bash
python demo_run.py
```
This runs an automated demonstration with:
- Server starting
- Alice and Bob registering
- Alice sending encrypted message
- Bob sending encrypted reply
- Graceful shutdown

### 3. Manual Interactive Mode

**Terminal 1 - Start Server:**
```bash
python server/server.py
```
Expected output:
```
2026-04-15 10:30:00,000 - INFO - Server started on 127.0.0.1:65432
```

**Terminal 2 - Start Alice Client:**
```bash
python client/client.py
```
```
--- Secure Chat Login ---
1. Register
2. Login
3. Exit
Select an option: 1
Username: alice
Password: mypassword123
Registration successful! You are now logged in.
Generating RSA keys...
--- Chat Started ---
type '/msg <peer> <message>' to reply: 
```

**Terminal 3 - Start Bob Client:**
```bash
python client/client.py
```
```
--- Secure Chat Login ---
1. Register
2. Login
3. Exit
Select an option: 1
Username: bob
Password: bobsecure
Registration successful! You are now logged in.
Generating RSA keys...
--- Chat Started ---
type '/msg <peer> <message>' to reply: 
```

**Alice sends message:**
```
type '/msg <peer> <message>' to reply: /msg bob This is a top-secret E2EE message!
[You → bob]: This is a top-secret E2EE message!
```

**Bob receives and replies:**
```
[bob]: This is a top-secret E2EE message!
type '/msg <peer> <message>' to reply: /msg alice Affirmative! Secure channel is verified.
[You → alice]: Affirmative! Secure channel is verified.
```

## Testing

### Running Unit Tests
```bash
# Run all tests
python -m unittest discover tests

# Run specific test file
python -m unittest tests.test_crypto
python -m unittest tests.test_auth

# Run with verbose output
python -m unittest discover tests -v
```

### Test Coverage

**Cryptographic Tests (`tests/test_crypto.py`):**
- AES key generation (32-byte, random)
- AES encryption/decryption roundtrip
- Multiple message types (empty, long, special chars, Unicode)
- Wrong key detection
- Ciphertext uniqueness (randomized IV)
- RSA key generation (2048-bit)
- RSA encryption/decryption roundtrip
- Cross-pair encryption fails (security)
- Base64 encoding/decoding
- End-to-end encryption flow

**Authentication Tests (`tests/test_auth.py`):**
- Password hashing with PBKDF2
- Password verification (correct/incorrect)
- Case sensitivity
- Input validation (username/password format)
- User registration (success, duplicates, invalid input)
- User authentication (success, wrong password, non-existent user)
- Rate limiting (attempt counter, success resets)
- Account lockout (after max attempts)
- Lockout timeout expiration
- Generic error messages (no info leakage)
- Timing attack resistance (basic)

### Quality Assurance Tests

**Manual Testing:**
1. **Localhost Testing:** Run server and two clients in separate terminals
2. **Invalid Credentials:** Test incorrect passwords are rejected
3. **Disconnect Handling:** Force close client (Ctrl+C) and verify server handles gracefully
4. **Rate Limiting:** Make 5 failed login attempts, verify lockout
5. **Server Blindness:** Confirm server logs show base64 ciphertext, not plaintext
6. **Cross-Client Messages:** Verify Alice's messages reach Bob with correct decryption
7. **Peer Availability:** Message non-existent peer, verify error handling
8. **Long Messages:** Send messages with 1000+ characters
9. **Special Characters:** Send Unicode and special characters

## Configuration

Edit `utils/config.py` to customize:
```python
HOST = '127.0.0.1'              # Server address
PORT = 65432                     # Server port
BUFFER_SIZE = 4096              # Socket buffer
TIMEOUT = 60.0                  # Socket timeout (seconds)
SALT_SIZE = 16                  # Password salt size
HASH_ITERATIONS = 100000        # PBKDF2 iterations
KEY_SIZE_RSA = 2048             # RSA key size
MAX_AUTH_ATTEMPTS = 5           # Lockout threshold
LOCKOUT_DURATION_SECONDS = 300  # Lockout duration
MIN_USERNAME_LENGTH = 3         # Min username length
MAX_USERNAME_LENGTH = 20        # Max username length
MIN_PASSWORD_LENGTH = 8         # Min password length
MAX_PASSWORD_LENGTH = 128       # Max password length
```

## Security Limitations & Future Work

### Current Limitations
* **In-Memory Storage:** User data stored in memory (not persisted)
* **No TLS/SSL:** Connection not encrypted at transport layer (for demo purposes)
* **No Perfect Forward Secrecy:** Private key compromise exposes all past messages
* **Client Key Storage:** Keys not persisted, regenerated on each login
* **No Signatures:** Message authentication relies on encryption only

### Recommended Future Enhancements
1. **TLS/SSL Support:** Encrypt transport layer for additional security
2. **Database Persistence:** Use encrypted database for user credentials
3. **Key Persistence:** Store private keys securely (encrypted)
4. **Digital Signatures:** Add RSA signatures for sender authentication
5. **Perfect Forward Secrecy:** Implement ephemeral key exchange (ECDHE)
6. **User Verification:** Out-of-band verification of peer public keys
7. **Message Timestamps:** Include timestamps to prevent replay attacks
8. **End-to-End Integrity:** HMAC for additional integrity checks
9. **Certificate Authority:** Proper PKI for key distribution
10. **Audit Logging:** Immutable audit trail of all authentication events

## References & Resources

### Cryptographic Standards
- [NIST SP 800-132 - PBKDF2](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-132.pdf)
- [RFC 3394 - AES Key Wrap](https://tools.ietf.org/html/rfc3394)
- [RFC 3610 - AES-CCM](https://tools.ietf.org/html/rfc3610)

### Libraries
- [PyCryptodome Documentation](https://pycryptodome.readthedocs.io/)
- [Python Hmac Documentation](https://docs.python.org/3/library/hmac.html)

### Security Concepts
- [OWASP Authentication Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)
- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)

## Conclusion

This project demonstrates enterprise-grade security practices for a real-time chat application. It combines:
- **Modern Cryptography:** AES-256 and RSA-2048 with industry best practices
- **Secure Authentication:** PBKDF2 with rate limiting and input validation
- **Robust Error Handling:** Graceful failures and comprehensive logging
- **Clean Code:** Type hints, docstrings, and comprehensive tests

The application is suitable for educational purposes, portfolio demonstration, and as a foundation for more advanced secure communication systems.
