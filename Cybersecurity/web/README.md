# Secure Chat Web Interface

Flask-based web client for the secure chat project.

## Features

- Register/login flow
- Encrypted message send and receive
- Security information panel (hashing/encryption settings)
- Message polling for near real-time updates

## Run

From `Cybersecurity/`:

```bash
pip install -r requirements.txt
python server/server.py
```

In another terminal:

```bash
cd Cybersecurity
python web/app.py
```

Open `http://127.0.0.1:5000`.

## Endpoints

- `GET /login`
- `GET /register`
- `GET /chat`
- `POST /api/send_message`
- `GET /api/get_messages`
- `GET /api/security_info`
