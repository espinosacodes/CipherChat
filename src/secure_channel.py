"""
CipherChat Secure Communication Channel
Provides end-to-end encrypted messaging with integrity verification.
"""

import json
import time
from datetime import datetime
from typing import Dict, Any, Optional, TYPE_CHECKING
from dataclasses import dataclass

from .crypto_engine import CryptoEngine
from .config import config
from .logger import logger
from .security import SecurityValidator, security_auditor
from .exceptions import MessageError, AuthenticationError, ValidationError

if TYPE_CHECKING:
    from .key_manager import KeyManager


@dataclass
class SecureMessage:
    """
    Represents a secure message with encryption and authentication.
    """
    sender: str
    recipient: str
    content: str  # Original plaintext (for sender)
    encrypted_data: Dict[str, str]
    signature: str
    timestamp: float
    
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
    def from_dict(cls, data: Dict[str, Any]) -> 'SecureMessage':
        """Create SecureMessage from dictionary."""
        # Validate required fields
        required_fields = ['sender', 'recipient', 'encrypted_data', 'signature', 'timestamp']
        for field in required_fields:
            if field not in data:
                raise ValidationError(f"Missing required field: {field}")
        
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
    
    def __init__(self, key_manager: 'KeyManager') -> None:
        """
        Initialize the secure channel.
        
        Args:
            key_manager: KeyManager instance for handling keys
        """
        self.key_manager = key_manager
        self.crypto_engine = CryptoEngine()
        logger.debug("SecureChannel initialized")
        
    def send_message(self, sender: str, recipient: str, message: str) -> Optional[SecureMessage]:
        """
        Create a secure message for transmission.
        
        Args:
            sender: Username of the sender
            recipient: Username of the recipient
            message: Plaintext message to send
            
        Returns:
            SecureMessage object or None if encryption fails
            
        Raises:
            MessageError: If message creation fails
            ValidationError: If input validation fails
            AuthenticationError: If authentication fails
        """
        try:
            # Input validation
            SecurityValidator.validate_username(sender)
            SecurityValidator.validate_username(recipient)
            SecurityValidator.validate_message_content(message)
            
            start_time = time.time()
            logger.info(f"Creating secure message from {sender} to {recipient}")
            
            # Load sender's private key for signing
            sender_private_key = self.key_manager.load_private_key(sender)
            if not sender_private_key:
                security_auditor.log_security_event('MISSING_PRIVATE_KEY', 
                                                   f'Private key not found for sender', sender)
                raise AuthenticationError(f"Private key not found for sender '{sender}'", sender)
            
            # Load recipient's public key for encryption
            recipient_public_key = self.key_manager.load_public_key(recipient)
            if not recipient_public_key:
                # Try to load from imported keys
                recipient_public_key = self.key_manager.load_imported_public_key(recipient)
                if not recipient_public_key:
                    security_auditor.log_security_event('MISSING_PUBLIC_KEY', 
                                                       f'Public key not found for recipient', recipient)
                    raise AuthenticationError(f"Public key not found for recipient '{recipient}'", recipient)
            
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
            
            duration = (time.time() - start_time) * 1000
            logger.info(f"✅ Message encrypted and signed successfully in {duration:.2f}ms")
            logger.log_performance("Message Creation", duration, f"from {sender} to {recipient}")
            
            security_auditor.log_security_event('MESSAGE_SENT', 
                                               f'Secure message sent to {recipient}', sender)
            
            return secure_message
            
        except (ValidationError, AuthenticationError):
            raise
        except Exception as e:
            security_auditor.log_security_event('MESSAGE_SEND_FAILED', str(e), sender)
            raise MessageError(f"Failed to create secure message: {str(e)}", "send")
    
    def receive_message(self, message_data: Dict[str, Any], recipient: str) -> Optional[str]:
        """
        Decrypt and verify a received message.
        
        Args:
            message_data: Dictionary containing the encrypted message
            recipient: Username of the recipient (for key lookup)
            
        Returns:
            Decrypted message content or None if verification fails
            
        Raises:
            MessageError: If message processing fails
            ValidationError: If input validation fails
            AuthenticationError: If authentication fails
        """
        try:
            # Input validation
            SecurityValidator.validate_username(recipient)
            
            if not message_data:
                raise ValidationError("Message data cannot be empty")
            
            start_time = time.time()
            logger.info(f"Processing received message for {recipient}")
            
            # Create SecureMessage from received data
            secure_message = SecureMessage.from_dict(message_data)
            
            # Validate sender
            SecurityValidator.validate_username(secure_message.sender)
            
            # Load recipient's private key for decryption
            recipient_private_key = self.key_manager.load_private_key(recipient)
            if not recipient_private_key:
                security_auditor.log_security_event('MISSING_PRIVATE_KEY', 
                                                   f'Private key not found for recipient', recipient)
                raise AuthenticationError(f"Private key not found for recipient '{recipient}'", recipient)
            
            # Load sender's public key for signature verification
            sender_public_key = self.key_manager.load_public_key(secure_message.sender)
            if not sender_public_key:
                # Try to load from imported keys
                sender_public_key = self.key_manager.load_imported_public_key(secure_message.sender)
                if not sender_public_key:
                    security_auditor.log_security_event('MISSING_PUBLIC_KEY', 
                                                       f'Public key not found for sender', secure_message.sender)
                    raise AuthenticationError(f"Public key not found for sender '{secure_message.sender}'", 
                                            secure_message.sender)
            
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
                security_auditor.log_security_event('INVALID_SIGNATURE', 
                                                   f'Message signature verification failed from {secure_message.sender}', 
                                                   recipient)
                raise AuthenticationError("Message signature verification failed!", secure_message.sender)
            
            # Check message age (prevent replay attacks)
            message_age = time.time() - secure_message.timestamp
            if message_age > config.session_timeout:
                security_auditor.log_security_event('EXPIRED_MESSAGE', 
                                                   f'Message too old: {message_age}s', recipient)
                logger.warning(f"Message from {secure_message.sender} is too old ({message_age:.1f}s)")
            
            duration = (time.time() - start_time) * 1000
            logger.info(f"✅ Message decrypted and verified successfully in {duration:.2f}ms")
            logger.log_performance("Message Processing", duration, f"from {secure_message.sender} to {recipient}")
            
            security_auditor.log_security_event('MESSAGE_RECEIVED', 
                                               f'Secure message received from {secure_message.sender}', recipient)
            
            return decrypted_message
            
        except (ValidationError, AuthenticationError):
            raise
        except Exception as e:
            security_auditor.log_security_event('MESSAGE_RECEIVE_FAILED', str(e), recipient)
            raise MessageError(f"Failed to process received message: {str(e)}", "receive")
    
    def create_key_exchange_message(self, sender: str, recipient: str) -> Optional[Dict[str, Any]]:
        """
        Create a secure key exchange message to establish trust.
        
        Args:
            sender: Username of the sender
            recipient: Username of the recipient
            
        Returns:
            Key exchange message dictionary or None if failed
            
        Raises:
            MessageError: If key exchange creation fails
            ValidationError: If input validation fails
            AuthenticationError: If authentication fails
        """
        try:
            # Input validation
            SecurityValidator.validate_username(sender)
            SecurityValidator.validate_username(recipient)
            
            start_time = time.time()
            logger.info(f"Creating key exchange message from {sender} to {recipient}")
            
            # Load sender's public key
            sender_public_key = self.key_manager.load_public_key(sender)
            if not sender_public_key:
                security_auditor.log_security_event('MISSING_PUBLIC_KEY', 
                                                   f'Public key not found for sender', sender)
                raise AuthenticationError(f"Public key not found for sender '{sender}'", sender)
            
            # Load sender's private key for signing
            sender_private_key = self.key_manager.load_private_key(sender)
            if not sender_private_key:
                security_auditor.log_security_event('MISSING_PRIVATE_KEY', 
                                                   f'Private key not found for sender', sender)
                raise AuthenticationError(f"Private key not found for sender '{sender}'", sender)
            
            # Create key exchange payload
            timestamp = time.time()
            key_exchange_payload: Dict[str, Any] = {
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
            
            duration = (time.time() - start_time) * 1000
            logger.info(f"✅ Key exchange message created for '{recipient}' in {duration:.2f}ms")
            logger.log_performance("Key Exchange Creation", duration)
            
            security_auditor.log_security_event('KEY_EXCHANGE_CREATED', 
                                               f'Key exchange message created for {recipient}', sender)
            
            return key_exchange_payload
            
        except (ValidationError, AuthenticationError):
            raise
        except Exception as e:
            security_auditor.log_security_event('KEY_EXCHANGE_FAILED', str(e), sender)
            raise MessageError(f"Failed to create key exchange message: {str(e)}", "key_exchange")
    
    def process_key_exchange(self, key_exchange_data: Dict[str, Any]) -> bool:
        """
        Process a received key exchange message.
        
        Args:
            key_exchange_data: Key exchange message data
            
        Returns:
            True if key exchange processed successfully, False otherwise
            
        Raises:
            MessageError: If key exchange processing fails
            ValidationError: If input validation fails
            AuthenticationError: If authentication fails
        """
        try:
            # Input validation
            if not key_exchange_data:
                raise ValidationError("Key exchange data cannot be empty")
            
            required_fields = ['sender', 'recipient', 'public_key', 'signature', 'timestamp']
            for field in required_fields:
                if field not in key_exchange_data:
                    raise ValidationError(f"Missing required field: {field}")
            
            start_time = time.time()
            sender = key_exchange_data['sender']
            recipient = key_exchange_data['recipient']
            
            # Validate usernames
            SecurityValidator.validate_username(sender)
            SecurityValidator.validate_username(recipient)
            
            logger.info(f"Processing key exchange from {sender} to {recipient}")
            
            public_key_pem = key_exchange_data['public_key'].encode('utf-8')
            signature = key_exchange_data['signature']
            timestamp = key_exchange_data['timestamp']
            
            # Check message age
            message_age = time.time() - timestamp
            if message_age > config.session_timeout:
                security_auditor.log_security_event('EXPIRED_KEY_EXCHANGE', 
                                                   f'Key exchange too old: {message_age}s', sender)
                raise AuthenticationError("Key exchange message is too old", sender)
            
            # Verify the signature using the provided public key
            payload_str = f"{sender}:{recipient}:{timestamp}"
            is_valid = self.crypto_engine.verify_signature(
                payload_str, 
                signature, 
                public_key_pem
            )
            
            if not is_valid:
                security_auditor.log_security_event('INVALID_KEY_EXCHANGE_SIGNATURE', 
                                                   f'Key exchange signature verification failed from {sender}')
                raise AuthenticationError("Key exchange signature verification failed!", sender)
            
            # Save the public key as an imported key
            import tempfile
            import os
            
            with tempfile.NamedTemporaryFile(mode='wb', delete=False, suffix='.pem') as temp_file:
                temp_file.write(public_key_pem)
                temp_file_path = temp_file.name
            
            try:
                success = self.key_manager.import_public_key(sender, temp_file_path)
                if success:
                    duration = (time.time() - start_time) * 1000
                    logger.info(f"✅ Key exchange processed successfully in {duration:.2f}ms")
                    logger.log_performance("Key Exchange Processing", duration)
                    
                    security_auditor.log_security_event('KEY_EXCHANGE_PROCESSED', 
                                                       f'Key exchange processed from {sender}', recipient)
                return success
            finally:
                os.unlink(temp_file_path)
                
        except (ValidationError, AuthenticationError):
            raise
        except Exception as e:
            security_auditor.log_security_event('KEY_EXCHANGE_PROCESS_FAILED', str(e))
            raise MessageError(f"Failed to process key exchange: {str(e)}", "key_exchange_process")
    
    def export_message_for_transmission(self, secure_message: SecureMessage) -> str:
        """
        Export a secure message as JSON string for transmission.
        
        Args:
            secure_message: SecureMessage to export
            
        Returns:
            JSON string representation of the message
            
        Raises:
            MessageError: If export fails
        """
        try:
            return json.dumps(secure_message.to_dict(), indent=2)
        except Exception as e:
            raise MessageError(f"Failed to export message: {str(e)}", "export")
    
    def import_message_from_transmission(self, message_json: str) -> Optional[Dict[str, Any]]:
        """
        Import a message from JSON string.
        
        Args:
            message_json: JSON string containing the message
            
        Returns:
            Message dictionary or None if parsing fails
            
        Raises:
            MessageError: If import fails
        """
        try:
            if not message_json:
                raise ValidationError("Message JSON cannot be empty")
            
            return json.loads(message_json)
        except json.JSONDecodeError as e:
            raise MessageError(f"Failed to parse message JSON: {str(e)}", "import")
        except Exception as e:
            raise MessageError(f"Failed to import message: {str(e)}", "import")