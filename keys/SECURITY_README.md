# SECURITY WARNING - PRIVATE KEYS DIRECTORY

## ⚠️ CRITICAL SECURITY INFORMATION

This directory contains cryptographic keys for CipherChat. 

### DO NOT:
- ❌ Commit private keys to version control
- ❌ Share private keys with anyone
- ❌ Store private keys in insecure locations
- ❌ Copy private keys to other systems without proper security
- ❌ Log or print private key contents

### DO:
- ✅ Keep private keys secure and confidential
- ✅ Use appropriate file permissions (600 for private keys)
- ✅ Backup private keys securely
- ✅ Rotate keys periodically
- ✅ Monitor for unauthorized access

### File Structure:
```
keys/
├── [username]/
│   ├── [username]_private.pem  # PRIVATE - Keep secure!
│   ├── [username]_public.pem   # PUBLIC - Can be shared
│   └── [username]_metadata.json
└── imported/
    └── [other_user]_public.pem  # PUBLIC keys from other users
```

### Permissions:
- Private key files: 600 (owner read/write only)
- Public key files: 644 (owner read/write, others read)
- Directories: 700 (owner read/write/execute only)

### Key Management:
- Generate new keys: `python cipherchat.py` → User Management → Create New User
- Export public key: `python cipherchat.py` → Key Management → Export My Public Key
- Import public key: `python cipherchat.py` → Key Management → Import Someone's Public Key

### Emergency Procedures:
If private keys are compromised:
1. Immediately revoke the compromised keys
2. Generate new key pairs for all affected users
3. Re-encrypt all messages with new keys
4. Notify all users to update their imported public keys
5. Investigate the security breach

### Security Best Practices:
- Use strong passphrases for key protection
- Store keys on encrypted storage
- Regular security audits
- Monitor access logs
- Keep software updated

For more information, see the Security Guide: `docs/SECURITY_GUIDE.md`
