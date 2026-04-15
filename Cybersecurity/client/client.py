# client/client.py
"""
Secure chat client with end-to-end encryption support.
Handles user authentication, key exchange, and encrypted messaging.
"""

import socket
import threading
import json
import sys
import os
import time
import logging
from typing import Optional, Dict

# Add parent directory to path to allow importing crypto modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.config import HOST, PORT, BUFFER_SIZE, TIMEOUT
from crypto.rsa import generate_rsa_key_pair, encrypt_with_public_key, decrypt_with_private_key
from crypto.aes import generate_aes_key, encrypt_aes, decrypt_aes

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class ChatClient:
    """
    Secure chat client with E2E encryption capabilities.
    
    Manages:
    - Server connection and authentication
    - RSA key pair generation
    - Encrypted message send/receive
    - Peer key caching
    """
    
    def __init__(self) -> None:
        """Initialize the chat client."""
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.private_key: Optional[bytes] = None
        self.public_key: Optional[bytes] = None
        self.username: Optional[str] = None
        self.peer_keys_cache: Dict[str, str] = {}  # peer_username -> public_key_pem
        self.running = True

    def connect(self) -> bool:
        """
        Connect to the chat server.
        
        Returns:
            bool: True if connection successful, False otherwise.
        """
        try:
            self.sock.connect((HOST, PORT))
            self.sock.settimeout(TIMEOUT)
            logger.info(f"Connected to server {HOST}:{PORT}")
            return True
        except (ConnectionRefusedError, OSError) as e:
            logger.error(f"Failed to connect to server: {e}")
            return False

    def authenticate(self) -> bool:
        """
        Authenticate user with server via registration or login.
        
        Prompts user to register or login, generates RSA key pair,
        and sends public key to server.
        
        Returns:
            bool: True if authentication successful, False otherwise.
        """
        while True:
            print("\n--- Secure Chat Login ---")
            print("1. Register")
            print("2. Login")
            print("3. Exit")
            choice = input("Select an option: ").strip()
            
            if choice == '3':
                return False
            
            if choice in ['1', '2']:
                username = input("Username: ").strip()
                password = input("Password: ")
                
                # Validate input (basic client-side check)
                if not username or not password:
                    print("Username and password cannot be empty.")
                    continue
                
                action = "register" if choice == '1' else "login"
                
                try:
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
                        
                        # Generate RSA key pair
                        logger.info("Generating RSA keys...")
                        print("Generating RSA keys...")
                        self.private_key, self.public_key = generate_rsa_key_pair()
                        
                        # Send public key to server
                        pub_req = json.dumps({"public_key": self.public_key.decode('utf-8')})
                        self.sock.sendall(pub_req.encode('utf-8'))
                        
                        logger.info(f"User {username} authenticated successfully")
                        return True
                    else:
                        print("Authentication failed. Please try again.")
                        logger.warning(f"Authentication failed for {action}:{username}")
                
                except (json.JSONDecodeError, socket.timeout, OSError) as e:
                    logger.error(f"Error during authentication: {e}")
                    print("Connection error. Please try again.")
            else:
                print("Invalid option. Please select 1, 2, or 3.")

    def receive_messages(self) -> None:
        """
        Receive and process messages from server in background thread.
        
        Handles:
        - Peer public key responses
        - Incoming encrypted messages
        - Server errors
        """
        while self.running:
            try:
                data = self.sock.recv(BUFFER_SIZE).decode('utf-8')
                if not data:
                    logger.info("Connection to server closed")
                    self.running = False
                    break
                
                try:
                    msg = json.loads(data)
                except json.JSONDecodeError:
                    logger.error("Received invalid JSON from server")
                    continue
                
                msg_type = msg.get("type")
                
                if msg_type == "peer_key":
                    # Store peer's public key
                    peer = msg.get("peer")
                    pub_key = msg.get("public_key")
                    if peer and pub_key:
                        self.peer_keys_cache[peer] = pub_key
                        logger.debug(f"Received public key for {peer}")
                
                elif msg_type == "incoming_msg":
                    # Decrypt and display incoming message
                    sender = msg.get("from")
                    payload = msg.get("payload")
                    
                    if not sender or not payload:
                        logger.warning("Received incomplete message")
                        continue
                    
                    try:
                        enc_session_key_b64 = payload.get("session_key")
                        ciphertext_b64 = payload.get("ciphertext")
                        iv_b64 = payload.get("iv")
                        
                        if not all([enc_session_key_b64, ciphertext_b64, iv_b64]):
                            logger.warning(f"Missing payload fields from {sender}")
                            continue
                        
                        # Decrypt AES session key using our RSA private key
                        session_key = decrypt_with_private_key(
                            enc_session_key_b64,
                            self.private_key
                        )
                        
                        # Decrypt message using AES session key
                        plaintext = decrypt_aes(ciphertext_b64, session_key, iv_b64)
                        
                        print(f"\n[{sender}]: {plaintext}")
                        print("type '/msg <peer> <message>' to reply: ", end="", flush=True)
                        
                    except Exception as e:
                        logger.error(f"Failed to decrypt message from {sender}: {e}")
                        print(f"\nFailed to decrypt message from {sender}")
                        print("type '/msg <peer> <message>' to reply: ", end="", flush=True)
                
                elif msg_type == "error":
                    # Display server error
                    error_msg = msg.get('message', 'Unknown error')
                    logger.warning(f"Server error: {error_msg}")
                    print(f"\nError: {error_msg}")
                    print("type '/msg <peer> <message>' to reply: ", end="", flush=True)
                
                else:
                    logger.warning(f"Unknown message type: {msg_type}")
            
            except socket.timeout:
                continue
            except Exception as e:
                if self.running:
                    logger.error(f"Error receiving message: {e}")
                break

    def get_peer_key(self, peer: str) -> Optional[bytes]:
        """
        Retrieve peer's public key from cache or server.
        
        Args:
            peer (str): Peer username.
        
        Returns:
            Optional[bytes]: Peer's public key in PEM format, or None if unavailable.
        """
        # Check cache first
        if peer in self.peer_keys_cache:
            return self.peer_keys_cache[peer].encode('utf-8')
        
        # Request from server
        try:
            req = json.dumps({"type": "get_user_key", "peer": peer})
            self.sock.sendall(req.encode('utf-8'))
            
            # Wait for key to arrive (with timeout)
            wait_time = 0
            max_wait = 50  # 5 seconds with 100ms intervals
            while peer not in self.peer_keys_cache and wait_time < max_wait:
                time.sleep(0.1)
                wait_time += 1
            
            if peer in self.peer_keys_cache:
                return self.peer_keys_cache[peer].encode('utf-8')
            
            logger.warning(f"Timeout waiting for {peer}'s public key")
            return None
        
        except Exception as e:
            logger.error(f"Error getting peer key for {peer}: {e}")
            return None

    def send_message(self, peer: str, message: str) -> None:
        """
        Send encrypted message to peer via server relay.
        
        Encryption flow:
        1. Get peer's RSA public key
        2. Generate random AES session key
        3. Encrypt message with AES session key
        4. Encrypt AES session key with peer's RSA public key
        5. Send encrypted payload via server
        
        Args:
            peer (str): Recipient username.
            message (str): Message to send.
        """
        try:
            # Get peer's public key
            peer_pub_key = self.get_peer_key(peer)
            if not peer_pub_key:
                print(f"Could not retrieve public key for {peer}. Are they online?")
                logger.warning(f"Cannot send message: {peer} key unavailable")
                return
            
            # Generate random AES session key
            session_key = generate_aes_key()
            
            # Encrypt message with AES session key
            ciphertext_b64, iv_b64 = encrypt_aes(message, session_key)
            
            # Encrypt AES session key with peer's RSA public key
            enc_session_key_b64 = encrypt_with_public_key(session_key, peer_pub_key)
            
            # Create and send payload
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
            print(f"[You → {peer}]: {message}")
            logger.info(f"Message sent from {self.username} to {peer}")
        
        except Exception as e:
            logger.error(f"Error sending message to {peer}: {e}")
            print(f"Error sending message: {e}")

    def chat_loop(self) -> None:
        """
        Main chat loop for user interaction.
        
        Commands:
        - /msg <peer_username> <message>: Send a secure message
        - /exit: Exit the application
        """
        print("\n--- Chat Started ---")
        print("Commands:")
        print("  /msg <peer_username> <message> - Send an encrypted message")
        print("  /exit - Exit the application")
        
        # Start message receiver thread
        receive_thread = threading.Thread(target=self.receive_messages, daemon=True)
        receive_thread.start()
        
        while self.running:
            try:
                user_in = input("type '/msg <peer> <message>' to reply: ").strip()
                
                if not user_in:
                    continue
                
                if user_in == "/exit":
                    self.running = False
                    print("Disconnecting...")
                    break
                
                if user_in.startswith("/msg"):
                    # Parse command: /msg <peer> <message>
                    parts = user_in.split(" ", 2)
                    if len(parts) < 3:
                        print("Usage: /msg <peer_username> <message>")
                        continue
                    
                    peer = parts[1].strip()
                    msg_text = parts[2].strip()
                    
                    if not peer or not msg_text:
                        print("Peer username and message cannot be empty.")
                        continue
                    
                    self.send_message(peer, msg_text)
                
                else:
                    print("Unknown command. Use '/msg <peer_username> <message>' or '/exit'")
            
            except KeyboardInterrupt:
                self.running = False
                break
            except Exception as e:
                logger.error(f"Error in chat loop: {e}")
                print(f"Error: {e}")
        
        # Cleanup
        try:
            self.sock.close()
        except Exception as e:
            logger.error(f"Error closing socket: {e}")
        
        print("Disconnected.")


def main() -> None:
    """Main entry point for the chat client."""
    client = ChatClient()
    try:
        if client.connect():
            if client.authenticate():
                client.chat_loop()
    except KeyboardInterrupt:
        logger.info("Client interrupted by user")
        print("\nClient disconnected.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")
    finally:
        try:
            client.sock.close()
        except Exception:
            pass


if __name__ == "__main__":
    main()
