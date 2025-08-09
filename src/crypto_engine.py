"""
CipherChat Cryptographic Engine
Implements hybrid encryption using RSA and AES for secure communication.
"""

import os
import json
import base64
import time
from typing import Tuple, Dict, Any, Optional
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.exceptions import InvalidSignature

from .config import config
from .logger import logger
from .exceptions import CryptographicError, ValidationError


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
        self.rsa_key_size = config.rsa_key_size
        self.aes_key_size = config.aes_key_size
        logger.debug(f"CryptoEngine initialized with RSA {self.rsa_key_size}-bit, AES {self.aes_key_size*8}-bit")
        
    def generate_rsa_key_pair(self) -> Tuple[bytes, bytes]:
        """
        Generate a new RSA key pair.
        
        Returns:
            Tuple of (private_key_pem, public_key_pem)
            
        Raises:
            CryptographicError: If key generation fails
        """
        try:
            start_time = time.time()
            logger.debug(f"Generating RSA key pair ({self.rsa_key_size} bits)")
            
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
            
            duration = (time.time() - start_time) * 1000
            logger.log_crypto_operation("RSA Key Generation", success=True)
            logger.log_performance("RSA Key Generation", duration)
            
            return private_pem, public_pem
            
        except Exception as e:
            logger.log_crypto_operation("RSA Key Generation", success=False)
            raise CryptographicError(f"Failed to generate RSA key pair: {str(e)}", "key_generation")
    
    def load_private_key(self, private_key_pem: bytes):
        """Load RSA private key from PEM format.
        
        Args:
            private_key_pem: Private key in PEM format
            
        Returns:
            Loaded private key object
            
        Raises:
            CryptographicError: If key loading fails
        """
        try:
            if not private_key_pem:
                raise ValidationError("Private key PEM data is empty")
                
            return serialization.load_pem_private_key(
                private_key_pem,
                password=None,
                backend=self.backend
            )
        except Exception as e:
            logger.error(f"Failed to load private key: {str(e)}")
            raise CryptographicError(f"Failed to load private key: {str(e)}", "key_loading")
    
    def load_public_key(self, public_key_pem: bytes):
        """Load RSA public key from PEM format.
        
        Args:
            public_key_pem: Public key in PEM format
            
        Returns:
            Loaded public key object
            
        Raises:
            CryptographicError: If key loading fails
        """
        try:
            if not public_key_pem:
                raise ValidationError("Public key PEM data is empty")
                
            return serialization.load_pem_public_key(
                public_key_pem,
                backend=self.backend
            )
        except Exception as e:
            logger.error(f"Failed to load public key: {str(e)}")
            raise CryptographicError(f"Failed to load public key: {str(e)}", "key_loading")
    
    def generate_aes_key(self) -> bytes:
        """Generate a random AES key.
        
        Returns:
            Random AES key bytes
            
        Raises:
            CryptographicError: If key generation fails
        """
        try:
            return os.urandom(self.aes_key_size)
        except Exception as e:
            logger.error(f"Failed to generate AES key: {str(e)}")
            raise CryptographicError(f"Failed to generate AES key: {str(e)}", "aes_key_generation")
    
    def encrypt_message(self, message: str, recipient_public_key_pem: bytes) -> Dict[str, str]:
        """
        Encrypt a message using hybrid encryption (RSA + AES).
        
        Args:
            message: The plaintext message to encrypt
            recipient_public_key_pem: Recipient's RSA public key in PEM format
            
        Returns:
            Dictionary containing encrypted message components
            
        Raises:
            CryptographicError: If encryption fails
            ValidationError: If input validation fails
        """
        try:
            # Input validation
            if not message:
                raise ValidationError("Message cannot be empty")
            
            if len(message.encode('utf-8')) > config.max_message_size:
                raise ValidationError(f"Message exceeds maximum size of {config.max_message_size} bytes")
            
            start_time = time.time()
            logger.debug(f"Encrypting message of length {len(message)}")
            
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
            
            duration = (time.time() - start_time) * 1000
            logger.log_crypto_operation("Message Encryption", success=True)
            logger.log_performance("Message Encryption", duration, f"size: {len(message)} chars")
            
            # Return encrypted data as base64 encoded strings
            return {
                'encrypted_message': base64.b64encode(encrypted_message).decode('utf-8'),
                'encrypted_key': base64.b64encode(encrypted_aes_key).decode('utf-8'),
                'iv': base64.b64encode(iv).decode('utf-8')
            }
            
        except (ValidationError, CryptographicError):
            raise
        except Exception as e:
            logger.log_crypto_operation("Message Encryption", success=False)
            raise CryptographicError(f"Failed to encrypt message: {str(e)}", "encryption")
    
    def decrypt_message(self, encrypted_data: Dict[str, str], private_key_pem: bytes) -> str:
        """
        Decrypt a message using hybrid decryption (RSA + AES).
        
        Args:
            encrypted_data: Dictionary with encrypted message components
            private_key_pem: Recipient's RSA private key in PEM format
            
        Returns:
            Decrypted plaintext message
            
        Raises:
            CryptographicError: If decryption fails
            ValidationError: If input validation fails
        """
        try:
            # Input validation
            if not encrypted_data:
                raise ValidationError("Encrypted data cannot be empty")
            
            required_keys = ['encrypted_message', 'encrypted_key', 'iv']
            for key in required_keys:
                if key not in encrypted_data:
                    raise ValidationError(f"Missing required key: {key}")
            
            start_time = time.time()
            logger.debug("Decrypting message")
            
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
            if padding_length > 16 or padding_length == 0:
                raise CryptographicError("Invalid padding detected", "decryption")
            
            message = padded_message[:-padding_length]
            
            duration = (time.time() - start_time) * 1000
            logger.log_crypto_operation("Message Decryption", success=True)
            logger.log_performance("Message Decryption", duration)
            
            return message.decode('utf-8')
            
        except (ValidationError, CryptographicError):
            raise
        except Exception as e:
            logger.log_crypto_operation("Message Decryption", success=False)
            raise CryptographicError(f"Failed to decrypt message: {str(e)}", "decryption")
    
    def sign_message(self, message: str, private_key_pem: bytes) -> str:
        """
        Create a digital signature for message authentication.
        
        Args:
            message: The message to sign
            private_key_pem: Signer's private key in PEM format
            
        Returns:
            Base64 encoded signature
            
        Raises:
            CryptographicError: If signing fails
            ValidationError: If input validation fails
        """
        try:
            # Input validation
            if not message:
                raise ValidationError("Message cannot be empty")
            
            start_time = time.time()
            logger.debug("Creating digital signature")
            
            private_key = self.load_private_key(private_key_pem)
            
            signature = private_key.sign(
                message.encode('utf-8'),
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=config.signature_salt_length
                ),
                hashes.SHA256()
            )
            
            duration = (time.time() - start_time) * 1000
            logger.log_crypto_operation("Message Signing", success=True)
            logger.log_performance("Message Signing", duration)
            
            return base64.b64encode(signature).decode('utf-8')
            
        except (ValidationError, CryptographicError):
            raise
        except Exception as e:
            logger.log_crypto_operation("Message Signing", success=False)
            raise CryptographicError(f"Failed to sign message: {str(e)}", "signing")
    
    def verify_signature(self, message: str, signature: str, public_key_pem: bytes) -> bool:
        """
        Verify a digital signature.
        
        Args:
            message: The original message
            signature: Base64 encoded signature
            public_key_pem: Signer's public key in PEM format
            
        Returns:
            True if signature is valid, False otherwise
            
        Raises:
            CryptographicError: If verification process fails
            ValidationError: If input validation fails
        """
        try:
            # Input validation
            if not message:
                raise ValidationError("Message cannot be empty")
            if not signature:
                raise ValidationError("Signature cannot be empty")
            
            start_time = time.time()
            logger.debug("Verifying digital signature")
            
            public_key = self.load_public_key(public_key_pem)
            signature_bytes = base64.b64decode(signature)
            
            try:
                public_key.verify(
                    signature_bytes,
                    message.encode('utf-8'),
                    padding.PSS(
                        mgf=padding.MGF1(hashes.SHA256()),
                        salt_length=config.signature_salt_length
                    ),
                    hashes.SHA256()
                )
                
                duration = (time.time() - start_time) * 1000
                logger.log_crypto_operation("Signature Verification", success=True)
                logger.log_performance("Signature Verification", duration)
                return True
                
            except InvalidSignature:
                duration = (time.time() - start_time) * 1000
                logger.log_security_event("INVALID_SIGNATURE", f"Signature verification failed for message")
                logger.log_performance("Signature Verification", duration)
                return False
                
        except (ValidationError, CryptographicError):
            raise
        except Exception as e:
            logger.log_crypto_operation("Signature Verification", success=False)
            raise CryptographicError(f"Failed to verify signature: {str(e)}", "verification")