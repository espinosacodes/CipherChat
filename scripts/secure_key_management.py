#!/usr/bin/env python3
"""
Secure Key Management Script for CipherChat
Handles secure generation, storage, and cleanup of cryptographic keys.
"""

import os
import sys
import shutil
import argparse
from pathlib import Path

def print_security_warning():
    """Print security warning about private keys."""
    print("🚨 SECURITY WARNING 🚨")
    print("=" * 50)
    print("Private cryptographic keys are highly sensitive!")
    print("NEVER commit private keys to version control.")
    print("NEVER share private keys with anyone.")
    print("NEVER store private keys in insecure locations.")
    print("=" * 50)
    print()

def check_git_status():
    """Check if private keys are being tracked by git."""
    try:
        import subprocess
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        
        sensitive_files = []
        for line in result.stdout.split('\n'):
            if line.strip() and any(pattern in line for pattern in 
                                   ['.pem', 'private', 'keys/', 'messages/']):
                sensitive_files.append(line.strip())
        
        if sensitive_files:
            print("⚠️  WARNING: Sensitive files detected in git status:")
            for file in sensitive_files:
                print(f"   {file}")
            print()
            return True
        return False
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("ℹ️  Git not available or not a git repository")
        return False

def secure_cleanup():
    """Securely remove all private keys and sensitive data."""
    print("🧹 Performing secure cleanup...")
    
    # Remove private key files
    key_patterns = [
        "keys/*/private.pem",
        "keys/*/*_private.pem", 
        "keys/*/private_key.pem",
        "keys/*/*_private_key.pem"
    ]
    
    for pattern in key_patterns:
        for file_path in Path(".").glob(pattern):
            if file_path.exists():
                print(f"🗑️  Removing: {file_path}")
                file_path.unlink()
    
    # Remove message files
    messages_dir = Path("messages")
    if messages_dir.exists():
        print(f"🗑️  Removing messages directory: {messages_dir}")
        shutil.rmtree(messages_dir)
    
    # Remove log files
    logs_dir = Path("logs")
    if logs_dir.exists():
        print(f"🗑️  Removing logs directory: {logs_dir}")
        shutil.rmtree(logs_dir)
    
    # Remove test directories
    test_dirs = ["test_keys", "test_messages", "test_logs"]
    for test_dir in test_dirs:
        test_path = Path(test_dir)
        if test_path.exists():
            print(f"🗑️  Removing test directory: {test_path}")
            shutil.rmtree(test_path)
    
    print("✅ Secure cleanup completed")

def setup_secure_directories():
    """Set up secure directories with proper permissions."""
    print("📁 Setting up secure directories...")
    
    directories = [
        "keys",
        "keys/imported", 
        "messages",
        "logs",
        "temp"
    ]
    
    for dir_path in directories:
        path = Path(dir_path)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
            # Set secure permissions (700 for directories)
            path.chmod(0o700)
            print(f"✅ Created: {path}")
        else:
            # Ensure existing directories have secure permissions
            path.chmod(0o700)
            print(f"✅ Secured: {path}")
    
    print("✅ Directory setup completed")

def verify_gitignore():
    """Verify that .gitignore contains necessary security exclusions."""
    print("🔍 Verifying .gitignore security exclusions...")
    
    gitignore_path = Path(".gitignore")
    if not gitignore_path.exists():
        print("❌ .gitignore file not found!")
        return False
    
    with open(gitignore_path, 'r') as f:
        content = f.read()
    
    required_patterns = [
        "*.pem",
        "keys/*/",
        "messages/",
        "logs/",
        "*.log",
        "*.json"
    ]
    
    missing_patterns = []
    for pattern in required_patterns:
        if pattern not in content:
            missing_patterns.append(pattern)
    
    if missing_patterns:
        print("❌ Missing security exclusions in .gitignore:")
        for pattern in missing_patterns:
            print(f"   - {pattern}")
        return False
    
    print("✅ .gitignore security exclusions verified")
    return True

def create_security_readme():
    """Create a security README for the keys directory."""
    security_readme = """# SECURITY WARNING - PRIVATE KEYS DIRECTORY

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
"""
    
    keys_dir = Path("keys")
    if keys_dir.exists():
        readme_path = keys_dir / "SECURITY_README.md"
        with open(readme_path, 'w') as f:
            f.write(security_readme)
        print(f"✅ Created security README: {readme_path}")

def main():
    """Main function for secure key management."""
    parser = argparse.ArgumentParser(description="Secure Key Management for CipherChat")
    parser.add_argument("--cleanup", action="store_true", 
                       help="Securely remove all private keys and sensitive data")
    parser.add_argument("--setup", action="store_true",
                       help="Set up secure directories with proper permissions")
    parser.add_argument("--verify", action="store_true",
                       help="Verify security configuration")
    parser.add_argument("--all", action="store_true",
                       help="Perform all security operations")
    
    args = parser.parse_args()
    
    print_security_warning()
    
    if args.cleanup or args.all:
        secure_cleanup()
    
    if args.setup or args.all:
        setup_secure_directories()
        create_security_readme()
    
    if args.verify or args.all:
        check_git_status()
        verify_gitignore()
    
    if not any([args.cleanup, args.setup, args.verify, args.all]):
        print("Usage: python scripts/secure_key_management.py --help")
        print("Recommended: python scripts/secure_key_management.py --all")

if __name__ == "__main__":
    main()
