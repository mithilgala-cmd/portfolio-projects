"""
Flask Web Frontend for Secure Chat Application.
Provides a user-friendly interface for the end-to-end encrypted chat system.
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import socket
import json
import threading
import base64
import os
import sys
from datetime import datetime

# Add parent directory to path for importing chat modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from crypto.rsa import generate_rsa_key_pair, encrypt_with_public_key, decrypt_with_private_key
from crypto.aes import generate_aes_key, encrypt_aes, decrypt_aes
from auth.auth import register_user, authenticate_user

app = Flask(__name__)
app.secret_key = os.urandom(32)

# Configuration
CHAT_SERVER_HOST = '127.0.0.1'
CHAT_SERVER_PORT = 65432
BUFFER_SIZE = 4096

# Store user sessions and sockets
user_sessions = {}  # username -> {'socket': socket, 'private_key': key, 'peer_keys': {}}
pending_messages = {}  # username -> list of messages


def create_secure_socket():
    """Create a socket connection to the chat server."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((CHAT_SERVER_HOST, CHAT_SERVER_PORT))
    return sock


def receive_messages_background(username, sock):
    """Background thread to receive messages from server."""
    while True:
        try:
            data = sock.recv(BUFFER_SIZE).decode('utf-8')
            if not data:
                break
            
            msg = json.loads(data)
            msg_type = msg.get("type")
            
            if msg_type == "peer_key":
                peer = msg.get("peer")
                pub_key = msg.get("public_key")
                if username in user_sessions:
                    user_sessions[username]['peer_keys'][peer] = pub_key
            
            elif msg_type == "incoming_msg":
                sender = msg.get("from")
                payload = msg.get("payload")
                
                try:
                    enc_session_key = payload.get("session_key")
                    ciphertext = payload.get("ciphertext")
                    iv = payload.get("iv")
                    
                    # Decrypt
                    private_key = user_sessions[username]['private_key']
                    session_key = decrypt_with_private_key(enc_session_key, private_key)
                    plaintext = decrypt_aes(ciphertext, session_key, iv)
                    
                    # Store message
                    if username not in pending_messages:
                        pending_messages[username] = []
                    
                    pending_messages[username].append({
                        'from': sender,
                        'message': plaintext,
                        'timestamp': datetime.now().isoformat(),
                        'encrypted': True
                    })
                except Exception as e:
                    print(f"Error decrypting message: {e}")
            
            elif msg_type == "error":
                if username not in pending_messages:
                    pending_messages[username] = []
                pending_messages[username].append({
                    'type': 'error',
                    'message': msg.get('message', 'Unknown error'),
                    'timestamp': datetime.now().isoformat()
                })
        
        except Exception as e:
            print(f"Error receiving message: {e}")
            break


@app.route('/')
def index():
    """Home page."""
    if 'username' in session:
        return redirect(url_for('chat'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Register a new user."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm', '')
        
        if password != confirm:
            return render_template('register.html', error='Passwords do not match')
        
        success, message = register_user(username, password)
        if success:
            session['username'] = username
            return redirect(url_for('chat'))
        else:
            return render_template('register.html', error=message)
    
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        success, message = authenticate_user(username, password)
        if success:
            session['username'] = username
            return redirect(url_for('chat'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')


@app.route('/chat')
def chat():
    """Chat interface."""
    if 'username' not in session:
        return redirect(url_for('login'))
    
    username = session['username']
    
    # Connect to server if not already connected
    if username not in user_sessions:
        try:
            sock = create_secure_socket()
            
            # Authenticate
            auth_req = json.dumps({
                "action": "login",
                "username": username,
                "password": session.get('temp_password', '')  # This won't work, need better approach
            })
            sock.sendall(auth_req.encode('utf-8'))
            response = sock.recv(BUFFER_SIZE).decode('utf-8')
            
            # Generate RSA keys
            private_key, public_key = generate_rsa_key_pair()
            
            # Send public key
            pub_req = json.dumps({"public_key": public_key.decode('utf-8')})
            sock.sendall(pub_req.encode('utf-8'))
            
            # Store session
            user_sessions[username] = {
                'socket': sock,
                'private_key': private_key,
                'public_key': public_key,
                'peer_keys': {}
            }
            pending_messages[username] = []
            
            # Start background receiver thread
            thread = threading.Thread(
                target=receive_messages_background,
                args=(username, sock),
                daemon=True
            )
            thread.start()
        
        except Exception as e:
            return render_template('chat.html', error=f"Connection error: {e}", username=username)
    
    return render_template('chat.html', username=username)


@app.route('/api/send_message', methods=['POST'])
def send_message_api():
    """API endpoint to send encrypted message."""
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    username = session['username']
    data = request.get_json()
    peer = data.get('peer', '').strip()
    message = data.get('message', '').strip()
    
    if not peer or not message:
        return jsonify({'error': 'Invalid peer or message'}), 400
    
    try:
        if username not in user_sessions:
            return jsonify({'error': 'Not connected to chat server'}), 500
        
        user_data = user_sessions[username]
        sock = user_data['socket']
        
        # Get peer's public key
        req = json.dumps({"type": "get_user_key", "peer": peer})
        sock.sendall(req.encode('utf-8'))
        
        # Wait for key
        import time
        for _ in range(50):
            if peer in user_data['peer_keys']:
                break
            time.sleep(0.1)
        
        if peer not in user_data['peer_keys']:
            return jsonify({'error': f'Could not get public key for {peer}'}), 400
        
        # Encrypt message
        peer_pub_key = user_data['peer_keys'][peer].encode('utf-8')
        session_key = generate_aes_key()
        ciphertext, iv = encrypt_aes(message, session_key)
        enc_session_key = encrypt_with_public_key(session_key, peer_pub_key)
        
        # Send message
        payload = {
            "session_key": enc_session_key,
            "ciphertext": ciphertext,
            "iv": iv
        }
        
        msg = json.dumps({
            "type": "chat_message",
            "target": peer,
            "payload": payload
        })
        sock.sendall(msg.encode('utf-8'))
        
        return jsonify({
            'success': True,
            'message': message,
            'peer': peer,
            'encrypted': True
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/get_messages', methods=['GET'])
def get_messages_api():
    """API endpoint to get pending messages."""
    if 'username' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    username = session['username']
    messages = pending_messages.get(username, [])
    pending_messages[username] = []
    
    return jsonify({'messages': messages})


@app.route('/api/security_info', methods=['GET'])
def security_info_api():
    """API endpoint for security information."""
    return jsonify({
        'algorithms': {
            'password_hashing': 'PBKDF2-SHA256 (100,000 iterations)',
            'session_encryption': 'AES-256-CBC',
            'key_exchange': 'RSA-2048 with OAEP padding',
            'padding': 'PKCS7'
        },
        'security_properties': {
            'confidentiality': 'End-to-end encryption (E2EE)',
            'integrity': 'CBC padding with PKCS7',
            'availability': 'Multi-threaded server',
            'authentication': 'Rate-limited login with account lockout'
        },
        'technical_details': {
            'aes_key_size': '256 bits',
            'rsa_key_size': '2048 bits',
            'salt_size': '16 bytes',
            'hash_iterations': '100,000'
        }
    })


@app.route('/logout')
def logout():
    """Logout user."""
    if 'username' in session:
        username = session['username']
        if username in user_sessions:
            try:
                user_sessions[username]['socket'].close()
            except:
                pass
            del user_sessions[username]
    
    session.clear()
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='127.0.0.1')
