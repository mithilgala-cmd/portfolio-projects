# Viva Preparation: Secure Chat Application

## 20 Likely Questions and Keyword Answers

1. **What is End-to-End Encryption (E2EE)?**
   *Answer:* Only the communicating users can read the messages; the server forwarding the traffic cannot decrypt them.
2. **Why do we use both RSA and AES (Hybrid Cryptography)?**
   *Answer:* RSA is slow but good for secure key exchange. AES is fast and efficient for encrypting bulk data (the actual message).
3. **What is the key size used for RSA in your project?**
   *Answer:* 2048-bit.
4. **What is the key size for AES in your project?**
   *Answer:* 256-bit (32 bytes).
5. **Which AES mode of operation did you use?**
   *Answer:* CBC (Cipher Block Chaining).
6. **Why do we need an IV (Initialization Vector) in AES-CBC?**
   *Answer:* To ensure that encrypting the same plaintext twice produces different ciphertexts, preventing pattern recognition.
7. **What is a "Salt" in password hashing?**
   *Answer:* Random data added to a password before hashing to defeat pre-computed dictionary or Rainbow Table attacks.
8. **What hashing algorithm did you use?**
   *Answer:* SHA-256.
9. **How does the Server know where to route the message?**
   *Answer:* The payload (JSON) contains a unencrypted "target" field, but the actual message contents are encrypted.
10. **Explain the Client registration process.**
    *Answer:* Client inputs password -> Client Sends to server -> Server hashes with salt -> Server stores Hash+Salt. (Note: in more advanced systems, hashing can happen client-side, but server-side is common for web systems).
11. **Where are the RSA keys generated?**
    *Answer:* Locally on the Client's machine after a successful login.
12. **What does the `.pem` format mean?**
    *Answer:* Privacy-Enhanced Mail. It is a Base64 encoded format used to store cryptographic keys safely.
13. **What happens if the server crashes?**
    *Answer:* Clients will throw a connection error and terminate gracefully based on our exception handling.
14. **Is this application resistant to a Man-in-the-Middle (MITM) attack?**
    *Answer:* Partially. The encryption protects the payload, but without PKI (Public Key Infrastructure / Certificates), an active MITM could theoretically swap public keys during exchange.
15. **What is `socket.AF_INET` and `socket.SOCK_STREAM`?**
    *Answer:* `AF_INET` means IPv4. `SOCK_STREAM` means TCP (Transmission Control Protocol).
16. **Why TCP and not UDP?**
    *Answer:* TCP is reliable and ensures ordered delivery, which is mandatory for encrypted streams and JSON packets so data isn't corrupted.
17. **What does `threading` do in your server?**
    *Answer:* It allows the server to `accept()` new clients and handle multiple active user connections simultaneously without blocking.
18. **What base encoding is used for sending binary data over JSON?**
    *Answer:* Base64.
19. **What is padding in block ciphers?**
    *Answer:* Adding extra bytes to the plaintext so it perfectly matches the cipher's block size (e.g., 16 bytes for AES).
20. **Can the server read user passwords?**
    *Answer:* It receives them during login, but it does not store them in plaintext; it only stores the SHA-256 hashes.

---

## 5 Difficult Cross-Questions

**1. Why AES + RSA and not just RSA for everything?**
*Answer:* RSA mathematically involves heavy prime-number exponentiation, which is too computationally expensive for long messages. It also has message size limits based on the key size. AES is a highly optimized symmetric stream that processes data extremely fast.

**2. Could the server administrator implement a code snippet to read the private keys?**
*Answer:* No. The RSA private keys are generated on the client machine and are *never* transmitted over the socket to the server. The server only ever receives the public keys.

**3. What specific attacks does your implementation prevent?**
*Answer:*
* Eavesdropping & Packet Sniffing (prevented by AES session encryption).
* Rainbow Table attacks (prevented by password salting).
* Database plaintext theft (prevented by SHA-256 hashing).

**4. What is the biggest limitation of your current architecture?**
*Answer:* The lack of digital signatures (non-repudiation) means Client A cannot *mathematically* prove Client B sent a message, only that it was encrypted with the correct keys. Also, the lack of Perfect Forward Secrecy means a compromised private key compromises all intercepted past messages.

**5. How would you upgrade this to support Perfect Forward Secrecy?**
*Answer:* I would implement a Diffie-Hellman Ephemeral (DHE) key exchange and rotate the symmetric keys continuously using something like the Double Ratchet algorithm (used by Signal/WhatsApp) instead of a static RSA key pair.
