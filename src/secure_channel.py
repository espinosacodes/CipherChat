"""
CipherChat Secure Communication Channel
Provides end-to-end encrypted messaging with integrity verification.
"""

import json
import time
from datetime import datetime
from typing import Dict, Any, Optional
from .crypto_engine import CryptoEngine
from .key_manager import KeyManager


class SecureMessage:
    """
    Represents a secure message with encryption and authentication.
    """
    
    def __init__(self, sender: str, recipient: str, content: str, 
                 encrypted_data: Dict[str, str], signature: str, timestamp: float):
        self.sender = sender
        self.recipient = recipient
        self.content = content  # Original plaintext (for sender)
        self.encrypted_data = encrypted_data
        self.signature = signature
        self.timestamp = timestamp
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert message to dictionary for transmission."""
        return {
            'sender': self.sender,
            'recipient': self.recipient,
            'encrypted_data': self.encrypted_data,
            'signature': self.signature,
            'timestamp': self.timestamp,
            'message_type': 'secure_message'
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """Create SecureMessage from dictionary."""
        return cls(
            sender=data['sender'],
            recipient=data['recipient'],
            content="",  # Will be decrypted later
            encrypted_data=data['encrypted_data'],
            signature=data['signature'],
            timestamp=data['timestamp']
        )
    
    def get_timestamp_str(self) -> str:
        """Get formatted timestamp string."""
        dt = datetime.fromtimestamp(self.timestamp)
        return dt.strftime("%Y-%m-%d %H:%M:%S")


class SecureChannel:
    """
    Manages secure communication between users with encryption and authentication.
    """
    
    def __init__(self, key_manager: KeyManager):
        """
        Initialize the secure channel.
        
        Args:
            key_manager: KeyManager instance for handling keys
        """
        self.key_manager = key_manager
        self.crypto_engine = CryptoEngine()
        
    def send_message(self, sender: str, recipient: str, message: str) -> Optional[SecureMessage]:
        """
        Create a secure message for transmission.
        
        Args:
            sender: Username of the sender
            recipient: Username of the recipient
            message: Plaintext message to send
            
        Returns:
            SecureMessage object or None if encryption fails
        """
        try:
            # Load sender's private key for signing
            sender_private_key = self.key_manager.load_private_key(sender)
            if not sender_private_key:
                print(f"❌ Private key not found for sender '{sender}'")
                return None
            
            # Load recipient's public key for encryption
            recipient_public_key = self.key_manager.load_public_key(recipient)
            if not recipient_public_key:
                # Try to load from imported keys
                recipient_public_key = self.key_manager.load_imported_public_key(recipient)
                if not recipient_public_key:
                    print(f"❌ Public key not found for recipient '{recipient}'")
                    return None
            
            # Create timestamp
            timestamp = time.time()
            
            # Create message payload for signing (includes metadata)
            message_payload = f"{sender}:{recipient}:{message}:{timestamp}"
            
            # Sign the message
            signature = self.crypto_engine.sign_message(message_payload, sender_private_key)
            
            # Encrypt the message
            encrypted_data = self.crypto_engine.encrypt_message(message, recipient_public_key)
            
            # Create secure message object
            secure_message = SecureMessage(
                sender=sender,
                recipient=recipient,
                content=message,
                encrypted_data=encrypted_data,
                signature=signature,
                timestamp=timestamp
            )
            
            print(f"✅ Message encrypted and signed successfully")
            return secure_message
            
        except Exception as e:
            print(f"❌ Failed to create secure message: {e}")
            return None
    
    def receive_message(self, message_data: Dict[str, Any], recipient: str) -> Optional[str]:
        """
        Decrypt and verify a received message.
        
        Args:
            message_data: Dictionary containing the encrypted message
            recipient: Username of the recipient (for key lookup)
            
        Returns:
            Decrypted message content or None if verification fails
        """
        try:
            # Create SecureMessage from received data
            secure_message = SecureMessage.from_dict(message_data)
            
            # Load recipient's private key for decryption
            recipient_private_key = self.key_manager.load_private_key(recipient)
            if not recipient_private_key:
                print(f"❌ Private key not found for recipient '{recipient}'")
                return None
            
            # Load sender's public key for signature verification
            sender_public_key = self.key_manager.load_public_key(secure_message.sender)
            if not sender_public_key:
                # Try to load from imported keys
                sender_public_key = self.key_manager.load_imported_public_key(secure_message.sender)
                if not sender_public_key:
                    print(f"❌ Public key not found for sender '{secure_message.sender}'")
                    return None
            
            # Decrypt the message
            decrypted_message = self.crypto_engine.decrypt_message(
                secure_message.encrypted_data, 
                recipient_private_key
            )
            
            # Verify the signature
            message_payload = f"{secure_message.sender}:{secure_message.recipient}:{decrypted_message}:{secure_message.timestamp}"
            is_valid = self.crypto_engine.verify_signature(
                message_payload, 
                secure_message.signature, 
                sender_public_key
            )
            
            if not is_valid:
                print(f"❌ Message signature verification failed!")
                return None
            
            print(f"✅ Message decrypted and verified successfully")
            return decrypted_message
            
        except Exception as e:
            print(f"❌ Failed to decrypt message: {e}")
            return None
    
    def create_key_exchange_message(self, sender: str, recipient: str) -> Optional[Dict[str, Any]]:
        """
        Create a secure key exchange message to establish trust.
        
        Args:
            sender: Username of the sender
            recipient: Username of the recipient
            
        Returns:
            Key exchange message dictionary or None if failed
        """
        try:
            # Load sender's public key
            sender_public_key = self.key_manager.load_public_key(sender)
            if not sender_public_key:
                print(f"❌ Public key not found for sender '{sender}'")
                return None
            
            # Load sender's private key for signing
            sender_private_key = self.key_manager.load_private_key(sender)
            if not sender_private_key:
                print(f"❌ Private key not found for sender '{sender}'")
                return None
            
            # Create key exchange payload
            timestamp = time.time()
            key_exchange_payload = {
                'sender': sender,
                'recipient': recipient,
                'public_key': sender_public_key.decode('utf-8'),
                'timestamp': timestamp,
                'message_type': 'key_exchange'
            }
            
            # Sign the key exchange message
            payload_str = f"{sender}:{recipient}:{timestamp}"
            signature = self.crypto_engine.sign_message(payload_str, sender_private_key)
            key_exchange_payload['signature'] = signature
            
            print(f"✅ Key exchange message created for '{recipient}'")
            return key_exchange_payload
            
        except Exception as e:
            print(f"❌ Failed to create key exchange message: {e}")
            return None
    
    def process_key_exchange(self, key_exchange_data: Dict[str, Any]) -> bool:
        """
        Process a received key exchange message.
        
        Args:
            key_exchange_data: Key exchange message data
            
        Returns:
            True if key exchange processed successfully, False otherwise
        """
        try:
            sender = key_exchange_data['sender']
            public_key_pem = key_exchange_data['public_key'].encode('utf-8')
            signature = key_exchange_data['signature']
            timestamp = key_exchange_data['timestamp']
            
            # Verify the signature using the provided public key
            payload_str = f"{sender}:{key_exchange_data['recipient']}:{timestamp}"
            is_valid = self.crypto_engine.verify_signature(
                payload_str, 
                signature, 
                public_key_pem
            )
            
            if not is_valid:
                print(f"❌ Key exchange signature verification failed!")
                return False
            
            # Save the public key as an imported key
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.pem') as temp_file:
                temp_file.write(public_key_pem)
                temp_file_path = temp_file.name
            
            try:
                success = self.key_manager.import_public_key(sender, temp_file_path)
                return success
            finally:
                os.unlink(temp_file_path)
                
        except Exception as e:
            print(f"❌ Failed to process key exchange: {e}")
            return False
    
    def export_message_for_transmission(self, secure_message: SecureMessage) -> str:
        """
        Export a secure message as JSON string for transmission.
        
        Args:
            secure_message: SecureMessage to export
            
        Returns:
            JSON string representation of the message
        """
        return json.dumps(secure_message.to_dict(), indent=2)
    
    def import_message_from_transmission(self, message_json: str) -> Optional[Dict[str, Any]]:
        """
        Import a message from JSON string.
        
        Args:
            message_json: JSON string containing the message
            
        Returns:
            Message dictionary or None if parsing fails
        """
        try:
            return json.loads(message_json)
        except json.JSONDecodeError as e:
            print(f"❌ Failed to parse message JSON: {e}")
            return None
