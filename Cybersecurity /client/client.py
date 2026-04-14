# client/client.py
import socket
import threading
import json
import sys
import os
import time

# Add parent directory to path to allow importing crypto modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import HOST, PORT, BUFFER_SIZE
from crypto.rsa import generate_rsa_key_pair, encrypt_with_public_key, decrypt_with_private_key
from crypto.aes import generate_aes_key, encrypt_aes, decrypt_aes

class ChatClient:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.private_key = None
        self.public_key = None
        self.username = None
        self.peer_keys_cache = {}  # peer_username -> public_key_pem
        self.running = True

    def connect(self):
        try:
            self.sock.connect((HOST, PORT))
            print(f"Connected to server {HOST}:{PORT}")
            return True
        except ConnectionRefusedError:
            print("Failed to connect to the server. Is it running?")
            return False

    def authenticate(self):
        while True:
            print("\n--- Secure Chat Login ---")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Select an option: ")
            
            if choice == '3':
                return False
                
            if choice in ['1', '2']:
                username = input("Username: ")
                password = input("Password: ")
                
                action = "register" if choice == '1' else "login"
                req = json.dumps({
                    "action": action,
                    "username": username,
                    "password": password
                })
                self.sock.sendall(req.encode('utf-8'))
                
                response = self.sock.recv(BUFFER_SIZE).decode('utf-8')
                resp_data = json.loads(response)
                
                if resp_data.get("status") == "success":
                    if action == "register":
                        print("Registration successful! You are now logged in.")
                    else:
                        print("Login successful!")
                        
                    self.username = username
                    
                    # Generate keys and share public key
                    print("Generating RSA keys...")
                    self.private_key, self.public_key = generate_rsa_key_pair()
                    
                    pub_req = json.dumps({"public_key": self.public_key.decode('utf-8')})
                    self.sock.sendall(pub_req.encode('utf-8'))
                    return True
                else:
                    print(f"Error: {resp_data.get('message', 'Authentication failed.')}")

    def receive_messages(self):
        while self.running:
            try:
                data = self.sock.recv(BUFFER_SIZE).decode('utf-8')
                if not data:
                    print("Connection to server closed.")
                    self.running = False
                    break
                    
                msg = json.loads(data)
                msg_type = msg.get("type")
                
                if msg_type == "peer_key":
                    peer = msg.get("peer")
                    pub_key = msg.get("public_key")
                    self.peer_keys_cache[peer] = pub_key
                    
                elif msg_type == "incoming_msg":
                    sender = msg.get("from")
                    payload = msg.get("payload")
                    
                    enc_session_key_b64 = payload.get("session_key")
                    ciphertext_b64 = payload.get("ciphertext")
                    iv_b64 = payload.get("iv")
                    
                    # 1. Decrypt AES session key using our RSA private key
                    try:
                        session_key = decrypt_with_private_key(enc_session_key_b64, self.private_key)
                        
                        # 2. Decrypt the actual message using the AES session key
                        plaintext = decrypt_aes(ciphertext_b64, session_key, iv_b64)
                        
                        print(f"\n[Peer] {sender}: {plaintext}\ntype '/msg <peer> <message>' to reply: ", end="", flush=True)
                    except Exception as e:
                        print(f"\nFailed to decrypt message from {sender}: {e}")
                elif msg_type == "error":
                    print(f"\nServer Error: {msg.get('message')}\ntype '/msg <peer> <message>' to reply: ", end="", flush=True)
            except BaseException as e:
                # Can be quite noisy during shutdown
                if self.running:
                    print(f"\nError receiving message: {e}")
                break

    def get_peer_key(self, peer: str):
        if peer in self.peer_keys_cache:
            return self.peer_keys_cache[peer].encode('utf-8')
            
        req = json.dumps({"type": "get_user_key", "peer": peer})
        self.sock.sendall(req.encode('utf-8'))
        
        # Wait for key to arrive
        wait_time = 0
        while peer not in self.peer_keys_cache and wait_time < 50:
            time.sleep(0.1)
            wait_time += 1
            
        if peer in self.peer_keys_cache:
            return self.peer_keys_cache[peer].encode('utf-8')
        return None

    def send_message(self, peer: str, message: str):
        # 1. Get Peer's public key
        peer_pub_key = self.get_peer_key(peer)
        if not peer_pub_key:
            print(f"Could not retrieve public key for {peer}. Are they online?")
            return
            
        # 2. Generate random AES Session Key
        session_key = generate_aes_key()
        
        # 3. Encrypt message with AES Session Key
        ciphertext_b64, iv_b64 = encrypt_aes(message, session_key)
        
        # 4. Encrypt AES Session Key with Peer's RSA Public Key
        enc_session_key_b64 = encrypt_with_public_key(session_key, peer_pub_key)
        
        # 5. Send payload via Server relay (Note: Server cannot decrypt this payload)
        payload = {
            "session_key": enc_session_key_b64,
            "ciphertext": ciphertext_b64,
            "iv": iv_b64
        }
        
        req = json.dumps({
            "type": "chat_message",
            "target": peer,
            "payload": payload
        })
        
        self.sock.sendall(req.encode('utf-8'))
        print(f"[You] to {peer}: {message}")

    def chat_loop(self):
        print("\n--- Chat Started ---")
        print("Commands:")
        print("  /msg <peer_username> <message> - Send a test message")
        print("  /exit - Exit the application")
        
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
        
        while self.running:
            try:
                user_in = input("type '/msg <peer> <message>' to reply: ")
                if not user_in.strip():
                    continue
                    
                if user_in == "/exit":
                    self.running = False
                    break
                    
                if user_in.startswith("/msg"):
                    parts = user_in.split(" ", 2)
                    if len(parts) < 3:
                        print("Usage: /msg <peer_username> <message>")
                        continue
                        
                    peer = parts[1]
                    msg_text = parts[2]
                    self.send_message(peer, msg_text)
                else:
                    print("Unknown command. Use /msg <peer_username> <message> or /exit")
            except KeyboardInterrupt:
                self.running = False
                break
                
        self.sock.close()
        print("Disconnected.")

if __name__ == "__main__":
    client = ChatClient()
    if client.connect():
        if client.authenticate():
            client.chat_loop()
