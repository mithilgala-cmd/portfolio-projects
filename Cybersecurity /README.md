Update: Added files on 13 April 2026. Also working on the cybersecurity project report.

# Secure Chat Application with End-to-End Encryption

## Overview
This is a comprehensive, secure chat application built in Python 3, demonstrating core cybersecurity concepts. It features End-to-End Encryption (E2EE), robust authentication with salted password hashing, and a client-server architecture where the server acts purely as a message relay without the ability to decrypt message contents.

## Features
* **End-to-End Encryption (E2EE):** AES Session Keys encrypted with RSA asymmetric cryptography.
* **Authentication:** Password salting and SHA-256 hashing.
* **Confidentiality:** Server only sees ciphertext.
* **Integrity:** Padded AES block modes.
* **Concurrency:** Multi-threaded client handling.

## Tech Stack
* Python 3.10+
* `socket`, `threading`, `json` (built-in)
* `pycryptodome` (Cryptography library for AES and RSA)

## Architecture

* **Client-Server Model:** Server relays encrypted payloads between clients.
* **Cryptography Flow:**
  `Client A → Generate AES Key → Encrypt message (AES) → Encrypt AES Key (Peer RSA Public) → Server (relay) → Client B → Decrypt AES Key (Own RSA Private) → Decrypt message (AES)`

```text
+----------+                                +---------+                                +----------+
|          | --(1) Auth & Send Pub Key----> |         | <---(1) Auth & Send Pub Key--- |          |
| Client A |                                | Server  |                                | Client B |
|          | --(2) Encrypted Payload -----> | (Relay) | ---(3) Relay Payload --------> |          |
+----------+                                +---------+                                +----------+
```

## Security Concepts (CIA Triad Mapping)
* **Confidentiality:** Provided via AES-256-CBC encryption of message payloads. The server operates in a zero-knowledge relay mode.
* **Integrity:** Ensured by CBC block padding and standard encryption schemas.
* **Availability:** TCP sockets and multi-threading allow multiple concurrent connections without crashing the server.

## Protocol Design
### Handshake
1. **Client connects:** Sends username and password either to register or login.
2. **Auth success:** Client generates RSA 2048-bit key pair and sends the public key to the server.
3. **Session Initiation:** When Client A messages Client B, Client A requests Client B's public key from the server.
4. **Key Exchange:** Client A generates a random AES 256-bit session key, encrypts it using B's public key, and attaches it to the message payload.
5. **Decryption:** Client B decrypts the session key using their private key and subsequently decrypts the message.

### Messaging Format (JSON)
```json
{
  "type": "chat_message",
  "target": "alice",
  "payload": {
    "session_key": "<base64_rsa_encrypted_aes_key>",
    "ciphertext": "<base64_aes_encrypted_message>",
    "iv": "<base64_aes_iv>"
  }
}
```

## Setup & Execution

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Server
```bash
python server/server.py
```
*Expected Output:*
```
2026-04-06 14:00:00,000 - INFO - Server started on 127.0.0.1:65432
```

### 3. Run the Clients
Open two separate terminal windows for two clients.
```bash
python client/client.py
```

### Sample Run
**Terminal 1 (Alice):**
```
--- Secure Chat Login ---
1. Register
Select an option: 1
Username: alice
Password: mypassword123
Registration successful! You are now logged in.
Generating RSA keys...
--- Chat Started ---
type '/msg <peer> <message>' to reply: /msg bob Hello Bob, this is Alice!
[You] to bob: Hello Bob, this is Alice!
```

**Terminal 2 (Bob):**
```
--- Secure Chat Login ---
1. Register
Select an option: 1
Username: bob
Password: securepass
Registration successful! You are now logged in.
Generating RSA keys...
--- Chat Started ---
[Peer] alice: Hello Bob, this is Alice!
type '/msg <peer> <message>' to reply: /msg alice Hi Alice! Decrypted successfully.
```

## Quality & Testing Plan
* **Localhost Testing:** Two terminals side-by-side using `127.0.0.1`.
* **Invalid Login:** Verify that entering incorrect passwords prevents connection.
* **Disconnect Handling:** Force close a client (`Ctrl+C`) and observe the server log gracefully handling the disconnect without crashing.
* **Server Blindness:** Modify the server code temporarily to print the `payload` received. Verify that it is unreadable base64 ciphertext and not plaintext.

## Demo & Screenshots
*(Instructor Note: Ensure you capture these specific views for your actual submission)*
* `screenshots/01_login_success.png` - Showing the initial auth screen and successful login message.
* `screenshots/02_key_exchange_log.png` - Showing the server's logging output when it securely receives the public keys.
* `screenshots/03_encrypted_payload.png` - (Optional) Printout on the server showing the JSON unreadable payload.
* `screenshots/04_decrypted_message.png` - The final UI showing "[Peer]: message".

## Optional Enhancements Included
1. **Password Salting:** Implemented randomized cryptographic salts stored with hashes.
2. **Dynamic Key Rotation:** A new AES session key is generated per transmission, providing pseudo-forward secrecy at a granular level.
