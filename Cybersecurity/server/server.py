# server/server.py
import socket
import threading
import json
import logging
import sys
import os

# Add parent directory to path to allow importing auth, etc.
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import HOST, PORT, BUFFER_SIZE
from auth.auth import register_user, authenticate_user

# Configure minimal basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Connected clients -> {"username": {"conn": socket, "public_key": "PEM..."}}
clients = {}
clients_lock = threading.Lock()

def handle_client(conn, addr):
    """Handle individual client connection."""
    logging.info(f"Connected by {addr}")
    current_user = None
    
    try:
        # Phase 1: Authentication / Registration
        auth_data = conn.recv(BUFFER_SIZE).decode('utf-8')
        if not auth_data:
            return
            
        req = json.loads(auth_data)
        action = req.get("action")
        username = req.get("username")
        password = req.get("password")
        
        if action == "register":
            success = register_user(username, password)
            conn.sendall(json.dumps({"status": "success" if success else "error"}).encode('utf-8'))
            if not success:
                return
        
        # After register or login, we treat login action as mandatory next step
        elif action == "login":
            success = authenticate_user(username, password)
            conn.sendall(json.dumps({"status": "success" if success else "error"}).encode('utf-8'))
            if not success:
               return 
        else:
            conn.sendall(json.dumps({"status": "error", "message": "invalid action"}).encode('utf-8'))
            return
            
        current_user = username
        
        # Wait for Public Key (sent right after login)
        pub_key_req = conn.recv(BUFFER_SIZE).decode('utf-8')
        pub_key_data = json.loads(pub_key_req)
        public_key = pub_key_data.get("public_key")
        
        with clients_lock:
            clients[current_user] = {"conn": conn, "public_key": public_key}
            
        logging.info(f"User {current_user} authenticated. Key received.")

        # Phase 2: Receive messages or act as relay
        while True:
            data = conn.recv(BUFFER_SIZE).decode('utf-8')
            if not data:
                break
                
            msg = json.loads(data)
            msg_type = msg.get("type")
            
            if msg_type == "get_user_key":
                # Requesting peer's public key
                peer = msg.get("peer")
                with clients_lock:
                    if peer in clients:
                        peer_key = clients[peer]["public_key"]
                        response = {"type": "peer_key", "peer": peer, "public_key": peer_key}
                    else:
                        response = {"type": "error", "message": "User not online"}
                conn.sendall(json.dumps(response).encode('utf-8'))
                
            elif msg_type == "chat_message":
                # Relaying chat message to target
                target = msg.get("target")
                payload = msg.get("payload") # This is a dict with encrypted AES sess key, ciphertext, etc
                
                with clients_lock:
                    if target in clients:
                        delivery_msg = {
                            "type": "incoming_msg",
                            "from": current_user,
                            "payload": payload
                        }
                        try:
                            clients[target]["conn"].sendall(json.dumps(delivery_msg).encode('utf-8'))
                        except Exception as e:
                            logging.error(f"Failed to deliver msg to {target}")
                    else:
                        err_msg = {"type": "error", "message": f"Target {target} offline"}
                        conn.sendall(json.dumps(err_msg).encode('utf-8'))
                        
    except Exception as e:
        # Client disconnect or parsing error
        pass
    finally:
        if current_user:
            with clients_lock:
                if current_user in clients:
                    del clients[current_user]
            logging.info(f"User {current_user} disconnected.")
        conn.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    logging.info(f"Server started on {HOST}:{PORT}")
    
    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.daemon = True
            thread.start()
    except KeyboardInterrupt:
        logging.info("Server shutting down.")
    finally:
        server.close()

if __name__ == "__main__":
    start_server()
