# Secure Chat (Cybersecurity Project)

A Python secure chat project demonstrating authentication, key exchange, and end-to-end encrypted messaging.

## What This Project Covers

- User registration and login with PBKDF2 hashing
- Rate limiting and temporary account lockout on failed logins
- RSA key-pair exchange between chat peers
- AES-based message encryption per message
- Server acting as a relay without plaintext message access
- Optional Flask web interface on top of the socket chat backend

## Tech Stack

- Python
- SQLite
- PyCryptodome
- Flask (web client)
- Socket programming + threading

## Structure

```text
Cybersecurity/
|-- auth/
|-- client/
|-- crypto/
|-- server/
|-- tests/
|-- utils/
|-- web/
|-- demo_run.py
|-- verify_database.py
`-- requirements.txt
```

## Run (CLI)

```bash
cd Cybersecurity
pip install -r requirements.txt
python server/server.py
```

In a second terminal:

```bash
cd Cybersecurity
python client/client.py
```

## Run (Web UI)

Start server first (`python server/server.py`), then in another terminal:

```bash
cd Cybersecurity
python web/app.py
```

Open `http://127.0.0.1:5000`.

## Tests

```bash
cd Cybersecurity
python -m pytest tests -v
```

## Notes

- Usernames are normalized to lowercase in the web flow.
- The project is designed for local/demo use and interview discussion, not production deployment.
