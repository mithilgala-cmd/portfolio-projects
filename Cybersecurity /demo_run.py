import subprocess
import time
import os
import sys

def main():
    print("--- Starting Server ---")
    server = subprocess.Popen(
        [sys.executable, "server/server.py"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    time.sleep(1.5) # Wait for server to bind

    print("--- Starting Client 1 (Alice) ---")
    alice = subprocess.Popen(
        [sys.executable, "client/client.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    print("--- Starting Client 2 (Bob) ---")
    bob = subprocess.Popen(
        [sys.executable, "client/client.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    # Register Alice
    alice.stdin.write("1\nalice\nmypassword123\n")
    alice.stdin.flush()
    # Need to wait long enough for RSA key generation and server to receive it alone
    time.sleep(3)

    # Register Bob
    bob.stdin.write("1\nbob\nbobsecure\n")
    bob.stdin.flush()
    time.sleep(3)

    # Alice messages Bob
    alice.stdin.write("/msg bob WARNING: This is a top-secret E2EE message!\n")
    alice.stdin.flush()
    time.sleep(2)

    # Bob messages Alice back
    bob.stdin.write("/msg alice Affirmative! Secure channel is verified.\n")
    bob.stdin.flush()
    time.sleep(2)

    # Exit Both
    alice.stdin.write("/exit\n")
    alice.stdin.flush()
    bob.stdin.write("/exit\n")
    bob.stdin.flush()
    
    time.sleep(1)
    server.terminate()

    print("\n================ SERVER LOGS ================")
    server_out, server_err = server.communicate()
    print(server_err)
    print(server_out)

    print("\n================ ALICE'S TERMINAL ================")
    alice_out, alice_err = alice.communicate()
    print(alice_out)

    print("\n================ BOB'S TERMINAL ================")
    bob_out, bob_err = bob.communicate()
    print(bob_out)

if __name__ == "__main__":
    main()
