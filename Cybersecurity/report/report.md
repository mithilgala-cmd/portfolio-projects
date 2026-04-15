# Project Report: Secure Chat Application with End-to-End Encryption

## Abstract
This project presents the design and implementation of a secure chat application emphasizing cryptographic principles and network security. Built using Python and the PyCryptodome library, the system provides End-to-End Encryption (E2EE) through an asymmetric/symmetric hybrid approach. It addresses confidentiality, authentication, and integrity, resulting in a reliable communication platform resistant to eavesdropping and localized data breaches.

## Introduction
With digital communication becoming ubiquitous, securing real-time data against interception is a critical priority. Standard chat applications lacking encryption are susceptible to Man-In-The-Middle (MITM) attacks and data sniffing. This project implements a robust Client-Server multi-threaded chat application to demonstrate how modern security layers—specifically RSA asymmetric key exchange and AES symmetric data encryption—can be integrated into network sockets.

## Literature Review
Existing protocols like TLS/SSL provide transport-layer security, while protocols like the Signal Protocol guarantee End-to-End Encryption. Research shows that hybrid cryptographic systems—combining the speed of symmetric ciphers (AES) with the secure key-distribution of asymmetric ciphers (RSA)—are the industry standard for maintaining secure chat infrastructures.

## Research Gap
While commercial frameworks exist, there is significant pedagogical value in building these layers natively from the socket level up. Many academic examples either omit proper E2EE (relying instead on server-side decryption) or ignore authentication salting, leaving systems vulnerable to rainbow table attacks and server compromise.

## Proposed Methodology
The implementation focuses on a strict separation of concerns where the central server acts solely as a relay for encrypted binary objects (encoded to base64) to maintain Zero-Knowledge of the message contents.
1. **Authentication Layer:** Handled via SHA-256 utilizing unique cryptographic salts.
2. **Key Exchance Layer:** Using purely 2048-bit RSA keys generated on the client upon login.
3. **Transport Layer:** Using AES-256-CBC, with a randomized Initialization Vector (IV) and a dynamically generated session key for each independent message burst.

## System Architecture
The network consists of a centralized Python socket server using Python's `threading` module to handle concurrent client connections dynamically.
When Client A wishes to message Client B, it first polls the server for Client B's cached RSA public key.
Once acquired, Client A hashes and encrypts the message locally. The generated JSON payload comprises the AES ciphertext alongside the AES Session Key (which is itself encrypted with Client B's RSA key). The server blindly routes this payload to Client B's established socket connection, where decryption occurs locally on Bob's hardware.

## Result & Discussion
The resulting application prevents the server administrator from ever viewing plaintext messages. The system flawlessly handles multiple concurrent sessions. Through testing, attempts to intercept the data across the sockets resulted only in the acquisition of highly randomized Base64 byte strings, proving the efficacy of the AES-CBC stream.

## Limitations
* No built-in Perfect Forward Secrecy (PFS) via continuous Diffie-Hellman ratcheting. If the permanent RSA private key is compromised, previous session keys encrypted with it (if captured) could be decrypted.
* Lacks robust digital signatures against impersonation after the authentication phase (Message Authentication Codes are not strictly enforced on the RSA keys themselves).

## Future Scope
* Implementation of the Double Ratchet Algorithm for robust Forward Secrecy.
* Adding a database (e.g., PostgreSQL or SQLite) for persistent user storage rather than an in-memory dictionary.
* Utilizing Digital Signatures to guarantee non-repudiation between peers.

## Conclusion
This Secure Chat Application actively demonstrates the CIA triad mapping correctly to modern programmatic logic. By successfully utilizing `hashlib`, `PyCryptodome`, and `socket` APIs, the project validates the feasibility of creating high-quality, heavily encrypted chat networks without relying on abstracted heavyweight frameworks.

## References
1. Stallings, W. (2017). *Cryptography and Network Security: Principles and Practice*, 7th Edition. Pearson.
2. "PyCryptodome Documentation." [Online]. Available: https://pycryptodome.readthedocs.io/.
3. Paar, C., & Pelzl, J. (2010). *Understanding Cryptography: A Textbook for Students and Practitioners*. Springer.
