"""
CipherChat Key Management System
Handles secure storage and retrieval of cryptographic keys.
"""

import os
import json
from typing import Optional, Tuple
from pathlib import Path
from .crypto_engine import CryptoEngine


class KeyManager:
    """
    Manages RSA key pairs for users including:
    - Key generation and storage
    - Key loading and validation
    - Secure key file management
    """
    
    def __init__(self, keys_directory: str = "keys"):
        """
        Initialize the key manager.
        
        Args:
            keys_directory: Directory to store key files
        """
        self.keys_dir = Path(keys_directory)
        self.keys_dir.mkdir(exist_ok=True)
        self.crypto_engine = CryptoEngine()
        
    def generate_user_keys(self, username: str) -> Tuple[str, str]:
        """
        Generate a new RSA key pair for a user.
        
        Args:
            username: The username for the key pair
            
        Returns:
            Tuple of (private_key_path, public_key_path)
        """
        # Generate key pair
        private_key_pem, public_key_pem = self.crypto_engine.generate_rsa_key_pair()
        
        # Create user directory
        user_dir = self.keys_dir / username
        user_dir.mkdir(exist_ok=True)
        
        # Save private key
        private_key_path = user_dir / f"{username}_private.pem"
        with open(private_key_path, 'wb') as f:
            f.write(private_key_pem)
        
        # Save public key
        public_key_path = user_dir / f"{username}_public.pem"
        with open(public_key_path, 'wb') as f:
            f.write(public_key_pem)
        
        # Set secure file permissions (read/write for owner only)
        os.chmod(private_key_path, 0o600)
        os.chmod(public_key_path, 0o644)
        
        # Save key metadata
        metadata = {
            'username': username,
            'private_key_file': f"{username}_private.pem",
            'public_key_file': f"{username}_public.pem",
            'key_size': self.crypto_engine.rsa_key_size
        }
        
        metadata_path = user_dir / f"{username}_metadata.json"
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"✅ Generated key pair for user '{username}'")
        print(f"   Private key: {private_key_path}")
        print(f"   Public key: {public_key_path}")
        
        return str(private_key_path), str(public_key_path)
    
    def load_private_key(self, username: str) -> Optional[bytes]:
        """
        Load a user's private key.
        
        Args:
            username: The username
            
        Returns:
            Private key in PEM format or None if not found
        """
        private_key_path = self.keys_dir / username / f"{username}_private.pem"
        
        if not private_key_path.exists():
            return None
            
        with open(private_key_path, 'rb') as f:
            return f.read()
    
    def load_public_key(self, username: str) -> Optional[bytes]:
        """
        Load a user's public key.
        
        Args:
            username: The username
            
        Returns:
            Public key in PEM format or None if not found
        """
        public_key_path = self.keys_dir / username / f"{username}_public.pem"
        
        if not public_key_path.exists():
            return None
            
        with open(public_key_path, 'rb') as f:
            return f.read()
    
    def user_exists(self, username: str) -> bool:
        """
        Check if a user has generated keys.
        
        Args:
            username: The username to check
            
        Returns:
            True if user exists, False otherwise
        """
        user_dir = self.keys_dir / username
        private_key_path = user_dir / f"{username}_private.pem"
        public_key_path = user_dir / f"{username}_public.pem"
        
        return private_key_path.exists() and public_key_path.exists()
    
    def list_users(self) -> list:
        """
        List all users with generated keys.
        
        Returns:
            List of usernames
        """
        users = []
        for user_dir in self.keys_dir.iterdir():
            if user_dir.is_dir() and self.user_exists(user_dir.name):
                users.append(user_dir.name)
        return sorted(users)
    
    def export_public_key(self, username: str, export_path: str = None) -> Optional[str]:
        """
        Export a user's public key to share with others.
        
        Args:
            username: The username
            export_path: Optional custom export path
            
        Returns:
            Path to exported public key file or None if user not found
        """
        public_key_pem = self.load_public_key(username)
        if not public_key_pem:
            return None
        
        if export_path is None:
            export_path = f"{username}_public_key.pem"
        
        with open(export_path, 'wb') as f:
            f.write(public_key_pem)
        
        print(f"✅ Exported public key for '{username}' to: {export_path}")
        return export_path
    
    def import_public_key(self, username: str, public_key_file: str) -> bool:
        """
        Import a public key from another user.
        
        Args:
            username: The username to associate with the key
            public_key_file: Path to the public key file
            
        Returns:
            True if import successful, False otherwise
        """
        try:
            # Verify it's a valid public key
            with open(public_key_file, 'rb') as f:
                public_key_pem = f.read()
            
            # Test loading the key to validate format
            self.crypto_engine.load_public_key(public_key_pem)
            
            # Create directory for imported keys
            imported_keys_dir = self.keys_dir / "imported"
            imported_keys_dir.mkdir(exist_ok=True)
            
            # Save the imported public key
            import_path = imported_keys_dir / f"{username}_public.pem"
            with open(import_path, 'wb') as f:
                f.write(public_key_pem)
            
            print(f"✅ Imported public key for '{username}' from: {public_key_file}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to import public key: {e}")
            return False
    
    def load_imported_public_key(self, username: str) -> Optional[bytes]:
        """
        Load an imported public key.
        
        Args:
            username: The username
            
        Returns:
            Public key in PEM format or None if not found
        """
        imported_key_path = self.keys_dir / "imported" / f"{username}_public.pem"
        
        if not imported_key_path.exists():
            return None
            
        with open(imported_key_path, 'rb') as f:
            return f.read()
    
    def delete_user_keys(self, username: str) -> bool:
        """
        Delete all keys for a user.
        
        Args:
            username: The username
            
        Returns:
            True if deletion successful, False otherwise
        """
        try:
            user_dir = self.keys_dir / username
            if user_dir.exists():
                import shutil
                shutil.rmtree(user_dir)
                print(f"✅ Deleted keys for user '{username}'")
                return True
            return False
        except Exception as e:
            print(f"❌ Failed to delete keys for '{username}': {e}")
            return False
