"""
Demo script for Secure Chat Application.

Demonstrates:
- Server startup
- Automated client registration
- Encrypted message exchange between two clients
- Graceful shutdown

This script runs a complete E2E encryption flow showing how users
can securely communicate without the server being able to decrypt messages.
"""

import subprocess
import time
import os
import sys
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def run_demo():
    """
    Run the secure chat demo with automated client interactions.
    """
    logger.info("Starting Secure Chat Application Demo...")
    
    # Start server
    logger.info("--- Starting Server ---")
    server = subprocess.Popen(
        [sys.executable, "server/server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    time.sleep(1.5)  # Wait for server to bind
    
    try:
        # Start Alice client
        logger.info("--- Starting Client 1 (Alice) ---")
        alice = subprocess.Popen(
            [sys.executable, "client/client.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Start Bob client
        logger.info("--- Starting Client 2 (Bob) ---")
        bob = subprocess.Popen(
            [sys.executable, "client/client.py"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Register Alice
        logger.info("Registering Alice...")
        alice.stdin.write("1\nalice\nmypassword123\n")
        alice.stdin.flush()
        time.sleep(3)  # Wait for RSA key generation and server processing
        
        # Register Bob
        logger.info("Registering Bob...")
        bob.stdin.write("1\nbob\nbobsecure\n")
        bob.stdin.flush()
        time.sleep(3)
        
        # Alice messages Bob
        logger.info("Alice sending encrypted message to Bob...")
        alice.stdin.write("/msg bob WARNING: This is a top-secret E2EE message!\n")
        alice.stdin.flush()
        time.sleep(2)
        
        # Bob messages Alice back
        logger.info("Bob sending encrypted message to Alice...")
        bob.stdin.write("/msg alice Affirmative! Secure channel is verified.\n")
        bob.stdin.flush()
        time.sleep(2)
        
        # Exit both clients
        logger.info("Closing clients...")
        alice.stdin.write("/exit\n")
        alice.stdin.flush()
        bob.stdin.write("/exit\n")
        bob.stdin.flush()
        
        time.sleep(1)
        
        logger.info("Demo complete. Shutting down server...")
        server.terminate()
        
        # Collect output
        print("\n" + "="*50)
        print("SERVER LOGS")
        print("="*50)
        server_out, server_err = server.communicate(timeout=5)
        print(server_err if server_err else server_out)
        
        print("\n" + "="*50)
        print("ALICE'S TERMINAL OUTPUT")
        print("="*50)
        alice_out, alice_err = alice.communicate()
        print(alice_out if alice_out else alice_err)
        
        print("\n" + "="*50)
        print("BOB'S TERMINAL OUTPUT")
        print("="*50)
        bob_out, bob_err = bob.communicate()
        print(bob_out if bob_out else bob_err)
        
        logger.info("Demo completed successfully!")
    
    except Exception as e:
        logger.error(f"Error during demo: {e}")
        server.terminate()
        if 'alice' in locals():
            alice.terminate()
        if 'bob' in locals():
            bob.terminate()
        raise
    
    except KeyboardInterrupt:
        logger.info("Demo interrupted by user")
        server.terminate()
        if 'alice' in locals():
            alice.terminate()
        if 'bob' in locals():
            bob.terminate()
        sys.exit(0)


if __name__ == "__main__":
    run_demo()
