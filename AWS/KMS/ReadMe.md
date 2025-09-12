1. **Introduction to AWS KMS**
   - What is AWS KMS?
   - Use cases for KMS
   - Benefits of using KMS

# Symmetric Encryption vs Asymmetric Encryption
### **Symmetric Encryption**

- **Definition**: Uses the **same key** for both **encryption** and **decryption**.
- **How it works**: 
  - You encrypt data with a secret key.
  - The same key is used to decrypt it.
- **Pros**:
  - Fast and efficient for large data.
  - Simple to implement.
- **Cons**:
  - Key must be securely shared and stored.
  - If the key is leaked, data is compromised.
- **Example**: AES (Advanced Encryption Standard)

### **Asymmetric Encryption**

- **Definition**: Uses a **pair of keys** — a **public key** to encrypt and a **private key** to decrypt.
- **How it works**:
  - Anyone can encrypt data using the public key.
  - Only the holder of the private key can decrypt it.
- **Pros**:
  - Secure key exchange — no need to share private key.
  - Enables digital signatures and authentication.
- **Cons**:
  - Slower than symmetric encryption.
  - Not ideal for encrypting large data directly.
- **Example**: RSA, ECC (Elliptic Curve Cryptography)

### Summary Table

| Feature              | Symmetric Encryption | Asymmetric Encryption |
|----------------------|----------------------|------------------------|
| Keys Used            | One (same key)       | Two (public & private) |
| Speed                | Fast                 | Slower                 |
| Security             | Depends on key secrecy | Secure key exchange   |
| Use Case             | Data encryption      | Secure communication, digital signatures |
| AWS KMS Support      | Default (AES-256)    | RSA & ECC key pairs    |

# How Encryption Works in **AWS KMS**

AWS Key Management Service (KMS) provides a secure and scalable way to encrypt data using **envelope encryption**. Here's a step-by-step explanation of how it works:

### **1. Envelope Encryption Concept**

Instead of encrypting your data directly with a KMS key, AWS KMS uses a two-step process:

- **Step 1**: KMS generates a **data key** (a temporary symmetric key).
- **Step 2**: You use this data key to encrypt your data locally.
- **Step 3**: The data key itself is encrypted using your **KMS key** (Customer Managed Key or CMK).

This approach improves performance and reduces the number of KMS API calls.

### **2. Encryption Workflow in AWS KMS**

#### **Encrypting Data**
1. **Call `GenerateDataKey` API**:
   - KMS returns:
     - A **plaintext data key** (used for encryption).
     - An **encrypted data key** (encrypted with your KMS key).
2. **Use the plaintext data key** to encrypt your data locally.
3. **Store the encrypted data key** along with your encrypted data.

#### **Decrypting Data**
1. **Retrieve the encrypted data key** from storage.
2. **Call `Decrypt` API**:
   - KMS decrypts the encrypted data key using your KMS key.
3. **Use the decrypted data key** to decrypt your data locally.

### **3. Direct Encryption (Optional)**

You can also use the `Encrypt` and `Decrypt` APIs to let KMS handle encryption directly, but this is typically used for small data (like secrets or tokens), not large files.

### **Supported Key Types**

- **Symmetric Keys (AES-256)**: Used for both encryption and decryption.
- **Asymmetric Keys (RSA, ECC)**:
  - Public key: Encrypt or verify.
  - Private key: Decrypt or sign.

### Data encryption at rest vs in transit

3. **KMS Key Types**
   - Customer Managed Keys (CMKs)
   - AWS Managed Keys
   - AWS Owned Keys

4. **Creating and Managing Keys**
   - How to create a KMS key
   - Key policies vs IAM policies
   - Key rotation (automatic vs manual)

5. **Basic Operations**
   - Encrypt and decrypt data using KMS
   - GenerateDataKey and GenerateDataKeyPair
   - Understanding envelope encryption

6. **KMS and IAM**
   - IAM roles and permissions for KMS
   - Fine-grained access control

7. **KMS Integration with AWS Services**
   - S3 (Server-side encryption with KMS)
   - EBS volumes
   - RDS and Aurora
   - Lambda and Secrets Manager

8. **Audit and Monitoring**
   - CloudTrail logging for KMS operations
   - Monitoring key usage and access patterns

9. **Security Best Practices**
   - Least privilege principle
   - Key separation and isolation
   - Using condition keys in policies

10. **Cross-Account Access**
   - Sharing KMS keys across AWS accounts
   - Resource-based policies for cross-account access

11. **Asymmetric Key Operations**
   - Signing and verification
   - Encryption and decryption with public/private keys

12. **Custom Key Stores**
   - AWS CloudHSM integration
   - When to use a custom key store

13. **Compliance and Regulatory Requirements**
   - FIPS 140-2 compliance
   - GDPR, HIPAA, and other standards

14. **Advanced Key Policy Design**
   - Delegating key administration
   - Complex policy conditions and constraints

15. **Performance and Cost Optimization**
   - Understanding KMS quotas and limits
   - Cost implications of KMS usage

16. **Disaster Recovery and Key Lifecycle**
   - Key deletion and recovery
   - Planning for key lifecycle and data retention

