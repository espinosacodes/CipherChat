"""
CipherChat Cryptographic Engine
Implements hybrid encryption using RSA and AES for secure communication.
"""

import os
import json
import base64
from typing import Tuple, Dict, Any
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend


class CryptoEngine:
    """
    Handles all cryptographic operations for CipherChat including:
    - RSA key pair generation and management
    - Hybrid encryption (RSA + AES)
    - Digital signatures for message authentication
    - Secure key exchange
    """
    
    def __init__(self):
        self.backend = default_backend()
        self.rsa_key_size = 2048
        self.aes_key_size = 32  # 256 bits
        
    def generate_rsa_key_pair(self) -> Tuple[bytes, bytes]:
        """
        Generate a new RSA key pair.
        
        Returns:
            Tuple of (private_key_pem, public_key_pem)
        """
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=self.rsa_key_size,
            backend=self.backend
        )
        
        # Serialize private key
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        # Serialize public key
        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return private_pem, public_pem
    
    def load_private_key(self, private_key_pem: bytes):
        """Load RSA private key from PEM format."""
        return serialization.load_pem_private_key(
            private_key_pem,
            password=None,
            backend=self.backend
        )
    
    def load_public_key(self, public_key_pem: bytes):
        """Load RSA public key from PEM format."""
        return serialization.load_pem_public_key(
            public_key_pem,
            backend=self.backend
        )
    
    def generate_aes_key(self) -> bytes:
        """Generate a random AES key."""
        return os.urandom(self.aes_key_size)
    
    def encrypt_message(self, message: str, recipient_public_key_pem: bytes) -> Dict[str, str]:
        """
        Encrypt a message using hybrid encryption (RSA + AES).
        
        Args:
            message: The plaintext message to encrypt
            recipient_public_key_pem: Recipient's RSA public key in PEM format
            
        Returns:
            Dictionary containing encrypted message components
        """
        # Load recipient's public key
        recipient_public_key = self.load_public_key(recipient_public_key_pem)
        
        # Generate random AES key
        aes_key = self.generate_aes_key()
        
        # Generate random IV for AES
        iv = os.urandom(16)  # 128 bits for AES-CBC
        
        # Encrypt the message with AES
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CBC(iv),
            backend=self.backend
        )
        encryptor = cipher.encryptor()
        
        # Pad message to be multiple of 16 bytes (AES block size)
        message_bytes = message.encode('utf-8')
        padding_length = 16 - (len(message_bytes) % 16)
        padded_message = message_bytes + bytes([padding_length]) * padding_length
        
        encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
        
        # Encrypt the AES key with RSA
        encrypted_aes_key = recipient_public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Return encrypted data as base64 encoded strings
        return {
            'encrypted_message': base64.b64encode(encrypted_message).decode('utf-8'),
            'encrypted_key': base64.b64encode(encrypted_aes_key).decode('utf-8'),
            'iv': base64.b64encode(iv).decode('utf-8')
        }
    
    def decrypt_message(self, encrypted_data: Dict[str, str], private_key_pem: bytes) -> str:
        """
        Decrypt a message using hybrid decryption (RSA + AES).
        
        Args:
            encrypted_data: Dictionary with encrypted message components
            private_key_pem: Recipient's RSA private key in PEM format
            
        Returns:
            Decrypted plaintext message
        """
        # Load private key
        private_key = self.load_private_key(private_key_pem)
        
        # Decode base64 data
        encrypted_message = base64.b64decode(encrypted_data['encrypted_message'])
        encrypted_aes_key = base64.b64decode(encrypted_data['encrypted_key'])
        iv = base64.b64decode(encrypted_data['iv'])
        
        # Decrypt the AES key with RSA
        aes_key = private_key.decrypt(
            encrypted_aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        
        # Decrypt the message with AES
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CBC(iv),
            backend=self.backend
        )
        decryptor = cipher.decryptor()
        
        padded_message = decryptor.update(encrypted_message) + decryptor.finalize()
        
        # Remove padding
        padding_length = padded_message[-1]
        message = padded_message[:-padding_length]
        
        return message.decode('utf-8')
    
    def sign_message(self, message: str, private_key_pem: bytes) -> str:
        """
        Create a digital signature for message authentication.
        
        Args:
            message: The message to sign
            private_key_pem: Signer's private key in PEM format
            
        Returns:
            Base64 encoded signature
        """
        private_key = self.load_private_key(private_key_pem)
        
        signature = private_key.sign(
            message.encode('utf-8'),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        
        return base64.b64encode(signature).decode('utf-8')
    
    def verify_signature(self, message: str, signature: str, public_key_pem: bytes) -> bool:
        """
        Verify a digital signature.
        
        Args:
            message: The original message
            signature: Base64 encoded signature
            public_key_pem: Signer's public key in PEM format
            
        Returns:
            True if signature is valid, False otherwise
        """
        try:
            public_key = self.load_public_key(public_key_pem)
            signature_bytes = base64.b64decode(signature)
            
            public_key.verify(
                signature_bytes,
                message.encode('utf-8'),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )
            return True
        except Exception:
            return False
