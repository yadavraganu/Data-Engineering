# SSL/TLS

**SSL (Secure Sockets Layer)** and its successor, **TLS (Transport Layer Security)**, are cryptographic protocols that provide **security** and **data integrity** for communications over computer networks, such as the internet.

While "SSL" is still a commonly used term, especially for digital certificates, all modern secure connections use the more advanced **TLS protocol**.

- **TLS** was developed to address vulnerabilities found in the older **SSL protocols**.
- All versions of **SSL** are now **deprecated** and **no longer considered secure**.

### TLS 1.2 Handshake: Step-by-Step Breakdown

To establish a secure connection between your browser (client) and a website's server, a **TLS handshake** takes place. While TLS 1.3 has streamlined this process, TLS 1.2 provides a more detailed view of how secure communication is established.

### 1. Client Hello
The browser initiates the handshake by sending a **Client Hello** message to the server. This message includes:

- The highest TLS version supported (e.g., TLS 1.2)
- A list of supported **cipher suites** (cryptographic algorithms)
- A random string of bytes called the **client random**

### 2. Server Hello
The server responds with a **Server Hello** message, selecting the strongest shared security options. It includes:

- The chosen TLS version
- The selected cipher suite
- A new random string called the **server random**
- The server’s **SSL/TLS certificate**

### 3. Authentication
The browser verifies the server’s certificate by checking:

- If it was issued by a trusted **Certificate Authority (CA)**
- If it is **valid** and not expired
- If the **domain name** matches the website’s address

### 4. Key Exchange
The client and server agree on a shared secret key for encryption:

- The client generates a **premaster secret**
- It encrypts this using the server’s **public key** (from the certificate)
- The encrypted premaster secret is sent to the server
- The server decrypts it using its **private key**
- Both parties use the **client random**, **server random**, and **premaster secret** to derive a **master secret**
- The master secret is used to generate **session keys** for symmetric encryption

### 5. Change Cipher Spec (Client)
The client sends a **Change Cipher Spec** message to indicate it will now use the newly established session keys for encryption.

### 6. Client Finished
The client sends an encrypted **Finished** message, verifying that the key exchange was successful.

### 7. Change Cipher Spec (Server)
The server sends its own **Change Cipher Spec** message to switch to encrypted communication.

### 8. Server Finished
The server sends an encrypted **Finished** message, completing the handshake.

### 9. Secure Communication Begins
The handshake is complete. All further communication between the client and server is encrypted using **symmetric encryption** with the shared session key.
