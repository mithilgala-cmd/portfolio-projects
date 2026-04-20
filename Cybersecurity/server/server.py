"""Secure chat server with E2E encryption support."""

import socket
import threading
import json
import logging
import sys
import os
from typing import Dict, Optional, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import HOST, PORT, BUFFER_SIZE, TIMEOUT
from utils.db import init_db_instance
from auth.auth import register_user, authenticate_user

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Initialize persistent database
db = init_db_instance()

clients: Dict[str, Dict[str, Any]] = {}
clients_lock = threading.Lock()
server_running = True


def handle_client(conn: socket.socket, addr: tuple) -> None:
    """Handle individual client connection with authentication and message relay."""
    logger.info(f"Connected by {addr}")
    current_user: Optional[str] = None
    
    try:
        conn.settimeout(TIMEOUT)
        
        auth_data = conn.recv(BUFFER_SIZE).decode('utf-8')
        if not auth_data:
            logger.warning(f"No auth data from {addr}")
            return
        
        try:
            req = json.loads(auth_data)
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON from {addr}")
            conn.sendall(json.dumps({"status": "error"}).encode('utf-8'))
            return
            
        action = req.get("action")
        username = req.get("username", "").strip()
        password = req.get("password", "")
        
        if action == "register":
            success, message = register_user(username, password)
            response = {"status": "success" if success else "error"}
            conn.sendall(json.dumps(response).encode('utf-8'))
            if not success:
                logger.warning(f"Registration failed for {username}")
                return
            logger.info(f"User {username} registered successfully")
        
        elif action == "login":
            success, message = authenticate_user(username, password)
            response = {"status": "success" if success else "error"}
            conn.sendall(json.dumps(response).encode('utf-8'))
            if not success:
                logger.warning(f"Login failed for {username}")
                return
            logger.info(f"User {username} authenticated successfully")
        
        else:
            conn.sendall(json.dumps({"status": "error"}).encode('utf-8'))
            logger.error(f"Invalid action from {addr}")
            return
        
        current_user = username
        
        try:
            pub_key_req = conn.recv(BUFFER_SIZE).decode('utf-8')
            pub_key_data = json.loads(pub_key_req)
            public_key = pub_key_data.get("public_key")
            
            if not public_key:
                logger.error(f"No public key provided by {username}")
                return
            
            with clients_lock:
                clients[current_user] = {"conn": conn, "public_key": public_key}
            
            logger.info(f"User {current_user} authenticated. Key received.")
        
        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Error receiving public key from {username}: {e}")
            return
        
        while server_running:
            try:
                data = conn.recv(BUFFER_SIZE).decode('utf-8')
                if not data:
                    logger.info(f"Client {current_user} disconnected")
                    break
                
                try:
                    msg = json.loads(data)
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON from {current_user}")
                    continue
                
                msg_type = msg.get("type")
                
                if msg_type == "get_user_key":
                    peer = msg.get("peer", "").strip()
                    
                    with clients_lock:
                        if peer in clients:
                            peer_key = clients[peer]["public_key"]
                            response = {"type": "peer_key", "peer": peer, "public_key": peer_key}
                            logger.debug(f"Providing public key for {peer} to {current_user}")
                        else:
                            response = {"type": "error", "message": "User offline"}
                            logger.debug(f"{peer} offline, request from {current_user}")
                    
                    conn.sendall(json.dumps(response).encode('utf-8'))
                
                elif msg_type == "chat_message":
                    target = msg.get("target", "").strip()
                    payload = msg.get("payload")
                    
                    if not payload:
                        logger.warning(f"Empty payload from {current_user} to {target}")
                        continue
                    
                    with clients_lock:
                        if target in clients:
                            delivery_msg = {"type": "incoming_msg", "from": current_user, "payload": payload}
                            try:
                                clients[target]["conn"].sendall(json.dumps(delivery_msg).encode('utf-8'))
                                logger.debug(f"Message relayed from {current_user} to {target}")
                            except Exception as e:
                                logger.error(f"Failed to deliver message to {target}: {e}")
                        else:
                            err_msg = {"type": "error", "message": "Target offline"}
                            conn.sendall(json.dumps(err_msg).encode('utf-8'))
                            logger.debug(f"{target} offline, message from {current_user}")
                
                else:
                    logger.warning(f"Unknown message type from {current_user}: {msg_type}")
            
            except socket.timeout:
                continue
            except Exception as e:
                logger.error(f"Error processing message from {current_user}: {e}")
                break
    
    except Exception as e:
        logger.error(f"Unexpected error in client handler: {e}")
    
    finally:
        if current_user:
            with clients_lock:
                if current_user in clients:
                    del clients[current_user]
            logger.info(f"User {current_user} removed from active clients")
        
        try:
            conn.close()
        except Exception as e:
            logger.error(f"Error closing connection: {e}")


def start_server() -> None:
    """Start the secure chat server listening for connections."""
    global server_running
    
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        logger.info(f"Server started on {HOST}:{PORT}")
        
        while server_running:
            try:
                conn, addr = server_socket.accept()
                thread = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
                thread.start()
            except Exception as e:
                if server_running:
                    logger.error(f"Error accepting connection: {e}")
    
    except KeyboardInterrupt:
        logger.info("Server shutting down...")
        server_running = False
    except OSError as e:
        logger.error(f"Server error: {e}")
    finally:
        server_running = False
        server_socket.close()
        logger.info("Server stopped")


if __name__ == "__main__":
    start_server()
