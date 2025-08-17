## Live Demo [Click here to view the app](https://cipherchat-qzui.onrender.com)

# 🔐 CipherChat - Secure Communication System

A comprehensive cybersecurity project that establishes secure communication channels between users using public-key cryptography. CipherChat implements end-to-end encryption with RSA and AES algorithms, ensuring confidentiality, integrity, and authenticity of messages.

## ✨ Key Features

- **🔑 Public-Key Encryption** - Each user has a public key (shared) and private key (kept secret)
- **🔒 Hybrid Encryption** - RSA + AES for optimal security and performance
- **🛡️ End-to-End Encryption** - Messages encrypted on sender's side, decrypted only by recipient
- **✍️ Digital Signatures** - Ensures message authenticity and tamper detection
- **🔄 Secure Key Exchange** - Safe public key sharing with verification
- **💬 Interactive CLI** - User-friendly command-line interface
- **📁 Message Storage** - Encrypted messages saved as portable files
- **🔍 Tamper Detection** - Automatic verification of message integrity

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐
│   Alice (User)  │    │   Bob (User)    │
├─────────────────┤    ├─────────────────┤
│ • Private Key   │    │ • Private Key   │
│ • Public Key    │    │ • Public Key    │
└─────────────────┘    └─────────────────┘
         │                       │
         │ 1. Key Exchange        │
         │ ←──────────────────→   │
         │                       │
         │ 2. Send Encrypted Msg │
         │ ────────────────────→  │
         │                       │
         │ 3. Send Reply         │
         │ ←────────────────────  │
         │                       │
```

### Security Implementation

1. **Key Generation**: 2048-bit RSA key pairs for each user
2. **Message Encryption**: 
   - Generate random 256-bit AES key
   - Encrypt message with AES-CBC
   - Encrypt AES key with recipient's RSA public key
3. **Message Authentication**:
   - Create digital signature using sender's RSA private key
   - Include timestamp and metadata in signature
4. **Transmission**: All components packaged in JSON format

## 🚀 Quick Start

### Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd CipherChat
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the interactive application:**
   ```bash
   python cipherchat.py
   ```

4. **Or run the demo:**
   ```bash
   python demo.py
   ```

### First Steps

1. **Create Users**: Generate key pairs for communication
2. **Exchange Keys**: Share public keys securely
3. **Send Messages**: Encrypt and transmit secure messages
4. **Receive Messages**: Decrypt and verify incoming messages

## 📖 Usage Guide

### Interactive Mode

Run the main application:
```bash
python cipherchat.py
```

Follow the menu system to:
- Create user accounts
- Manage cryptographic keys
- Send encrypted messages
- Receive and decrypt messages
- Exchange public keys

### Demo Mode

Experience CipherChat capabilities:
```bash
# Basic demo
python demo.py

# Performance testing
python demo.py --performance

# Full demo with performance tests
python demo.py --full
```

### Programmatic Usage

```python
from src.key_manager import KeyManager
from src.secure_channel import SecureChannel

# Initialize components
key_manager = KeyManager()
secure_channel = SecureChannel(key_manager)

# Generate keys for users
key_manager.generate_user_keys("alice")
key_manager.generate_user_keys("bob")

# Send encrypted message
message = secure_channel.send_message("alice", "bob", "Hello Bob!")

# Decrypt message
decrypted = secure_channel.receive_message(message.to_dict(), "bob")
```

## 🔧 Technical Details

### Cryptographic Algorithms

| Component | Algorithm | Key Size | Purpose |
|-----------|-----------|----------|---------|
| Asymmetric Encryption | RSA | 2048-bit | Key exchange, signatures |
| Symmetric Encryption | AES-CBC | 256-bit | Message encryption |
| Padding | OAEP | SHA-256 | RSA encryption padding |
| Signatures | PSS | SHA-256 | Message authentication |
| Hashing | SHA-256 | - | Integrity verification |

### File Structure

```
CipherChat/
├── src/
│   ├── __init__.py
│   ├── crypto_engine.py      # Core cryptographic operations
│   ├── key_manager.py        # Key generation and storage
│   ├── secure_channel.py     # Secure messaging protocol
│   └── chat_interface.py     # Interactive CLI interface
├── keys/                     # Generated user keys
│   ├── [username]/
│   │   ├── [username]_private.pem
│   │   ├── [username]_public.pem
│   │   └── [username]_metadata.json
│   └── imported/             # Imported public keys
├── messages/                 # Encrypted message files
├── cipherchat.py            # Main application entry point
├── demo.py                  # Demonstration script
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

### Security Features

- **Forward Secrecy**: Each message uses a unique AES key
- **Tamper Detection**: Digital signatures prevent message modification
- **Key Isolation**: Private keys never transmitted
- **Secure Storage**: Keys stored with appropriate file permissions
- **Metadata Protection**: Timestamps prevent replay attacks

## 🛡️ Security Analysis

### Threat Model

**Protected Against:**
- ✅ Eavesdropping (passive monitoring)
- ✅ Message tampering (active modification)
- ✅ Identity spoofing (impersonation)
- ✅ Replay attacks (message reuse)

**Assumptions:**
- Private keys remain secure on user devices
- System time is reasonably accurate
- Python cryptographic libraries are secure

### Cryptographic Properties

1. **Confidentiality**: RSA + AES hybrid encryption
2. **Integrity**: SHA-256 hashing and digital signatures  
3. **Authenticity**: RSA-PSS signatures with private keys
4. **Non-repudiation**: Cryptographic proof of message origin

## 🧪 Testing

Run the comprehensive demo to verify all features:

```bash
python demo.py
```

This demonstrates:
- Key generation and exchange
- Message encryption/decryption
- Digital signature verification
- Tamper detection
- Performance benchmarks

## 📋 Dependencies

- **cryptography** (>=41.0.0): Core cryptographic operations
- **pycryptodome** (>=3.19.0): Additional crypto utilities
- **colorama** (>=0.4.6): Terminal colors (optional)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Implement security improvements
4. Add comprehensive tests
5. Submit a pull request

## 📄 License

## ⚠️ CRITICAL SECURITY WARNING

### 🚨 Private Key Security
**NEVER commit private cryptographic keys to version control!**

- Private key files (`.pem`) contain highly sensitive information
- If private keys are exposed, immediately revoke and regenerate them
- Use the security tools provided: `python scripts/secure_key_management.py --all`
- Follow the Security Checklist: `docs/SECURITY_CHECKLIST.md`

### 🔒 Security Best Practices
- Keep private keys secure and confidential
- Use appropriate file permissions (600 for private keys)
- Never share private keys with anyone
- Regularly audit your security configuration
- Monitor for unauthorized access

### 🛡️ Security Tools
```bash
# Security verification
python scripts/secure_key_management.py --verify

# Secure cleanup
python scripts/secure_key_management.py --cleanup

# Complete security setup
python scripts/secure_key_management.py --all
```

## ⚠️ Disclaimer

This software is for educational and research purposes. While implementing industry-standard cryptographic algorithms and security measures, it has not undergone professional security audit. Use in production environments at your own risk.

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## ⚠️ Disclaimer

This software is for educational and research purposes. While implementing industry-standard cryptographic algorithms, it has not undergone professional security audit. Use in production environments at your own risk.

## 🔗 References

- [RFC 3447 - RSA PKCS #1](https://tools.ietf.org/html/rfc3447)
- [NIST SP 800-38A - AES Modes](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38a.pdf)
- [Python Cryptography Library](https://cryptography.io/)

---

**🔐 Stay Secure! Use CipherChat for your confidential communications.**
