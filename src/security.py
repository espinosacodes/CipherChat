"""
CipherChat Security Utilities
Provides additional security features and validation functions.
"""

import os
import re
import hashlib
import secrets
import time
from typing import Optional, Dict, Any, List
from pathlib import Path

from .config import config
from .logger import logger
from .exceptions import SecurityError, ValidationError


class SecurityValidator:
    """Security validation utilities for CipherChat."""
    
    # Security constants
    MIN_USERNAME_LENGTH = 3
    MAX_USERNAME_LENGTH = 32
    USERNAME_PATTERN = re.compile(r'^[a-zA-Z0-9_-]+$')
    
    # File size limits
    MAX_KEY_FILE_SIZE = 10 * 1024  # 10KB
    MAX_MESSAGE_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    
    @classmethod
    def validate_username(cls, username: str) -> bool:
        """
        Validate username for security and usability.
        
        Args:
            username: Username to validate
            
        Returns:
            True if valid, False otherwise
            
        Raises:
            ValidationError: If username is invalid
        """
        if not username:
            raise ValidationError("Username cannot be empty")
        
        if len(username) < cls.MIN_USERNAME_LENGTH:
            raise ValidationError(f"Username must be at least {cls.MIN_USERNAME_LENGTH} characters")
        
        if len(username) > cls.MAX_USERNAME_LENGTH:
            raise ValidationError(f"Username must be at most {cls.MAX_USERNAME_LENGTH} characters")
        
        if not cls.USERNAME_PATTERN.match(username):
            raise ValidationError("Username can only contain letters, numbers, hyphens, and underscores")
        
        # Check for reserved usernames
        reserved_names = ['admin', 'root', 'system', 'config', 'test', 'null', 'undefined']
        if username.lower() in reserved_names:
            raise ValidationError(f"Username '{username}' is reserved")
        
        return True
    
    @classmethod
    def validate_file_path(cls, file_path: str, max_size: Optional[int] = None) -> bool:
        """
        Validate file path for security.
        
        Args:
            file_path: Path to validate
            max_size: Maximum file size in bytes
            
        Returns:
            True if valid, False otherwise
            
        Raises:
            SecurityError: If path is unsafe
            ValidationError: If file is invalid
        """
        if not file_path:
            raise ValidationError("File path cannot be empty")
        
        path = Path(file_path)
        
        # Check for path traversal attempts
        try:
            path.resolve()
        except (OSError, ValueError) as e:
            raise SecurityError(f"Invalid file path: {e}")
        
        # Check for dangerous path components
        dangerous_patterns = ['..', '~', '$', '|', ';', '&', '`']
        for pattern in dangerous_patterns:
            if pattern in str(path):
                raise SecurityError(f"Dangerous path component detected: {pattern}")
        
        # Check file exists if validation is for existing file
        if not path.exists():
            return True  # Allow for new file creation
        
        # Check file size
        if max_size and path.is_file():
            file_size = path.stat().st_size
            if file_size > max_size:
                raise ValidationError(f"File exceeds maximum size of {max_size} bytes")
        
        return True
    
    @classmethod
    def validate_message_content(cls, message: str) -> bool:
        """
        Validate message content for security.
        
        Args:
            message: Message content to validate
            
        Returns:
            True if valid, False otherwise
            
        Raises:
            ValidationError: If message is invalid
        """
        if not message:
            raise ValidationError("Message cannot be empty")
        
        # Check message size
        message_bytes = message.encode('utf-8')
        if len(message_bytes) > config.max_message_size:
            raise ValidationError(f"Message exceeds maximum size of {config.max_message_size} bytes")
        
        # Check for suspicious patterns (basic XSS/injection prevention)
        suspicious_patterns = [
            r'<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>',
            r'javascript:',
            r'data:text\/html',
            r'vbscript:',
        ]
        
        for pattern in suspicious_patterns:
            if re.search(pattern, message, re.IGNORECASE):
                logger.log_security_event("SUSPICIOUS_MESSAGE_CONTENT", 
                                         f"Suspicious pattern detected in message")
                # Don't raise error, just log for monitoring
        
        return True


class SecureRandom:
    """Cryptographically secure random number generation utilities."""
    
    @staticmethod
    def generate_token(length: int = 32) -> str:
        """Generate a cryptographically secure random token."""
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_nonce(length: int = 16) -> bytes:
        """Generate a cryptographically secure random nonce."""
        return secrets.token_bytes(length)
    
    @staticmethod
    def generate_salt(length: int = 32) -> bytes:
        """Generate a cryptographically secure random salt."""
        return secrets.token_bytes(length)


class IntegrityChecker:
    """File and data integrity checking utilities."""
    
    @staticmethod
    def calculate_file_hash(file_path: str, algorithm: str = 'sha256') -> str:
        """
        Calculate hash of a file for integrity checking.
        
        Args:
            file_path: Path to the file
            algorithm: Hash algorithm to use
            
        Returns:
            Hexadecimal hash string
        """
        hash_obj = hashlib.new(algorithm)
        
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_obj.update(chunk)
        except IOError as e:
            logger.error(f"Failed to read file for hashing: {e}")
            raise SecurityError(f"Failed to calculate file hash: {e}")
        
        return hash_obj.hexdigest()
    
    @staticmethod
    def verify_file_integrity(file_path: str, expected_hash: str, algorithm: str = 'sha256') -> bool:
        """
        Verify file integrity against expected hash.
        
        Args:
            file_path: Path to the file
            expected_hash: Expected hash value
            algorithm: Hash algorithm used
            
        Returns:
            True if integrity is verified, False otherwise
        """
        try:
            actual_hash = IntegrityChecker.calculate_file_hash(file_path, algorithm)
            return secrets.compare_digest(actual_hash, expected_hash)
        except SecurityError:
            return False


class SecurityAuditor:
    """Security auditing and monitoring utilities."""
    
    def __init__(self):
        self.security_events: List[Dict[str, Any]] = []
    
    def log_security_event(self, event_type: str, details: str, username: Optional[str] = None) -> None:
        """Log a security event for auditing."""
        event = {
            'timestamp': time.time(),
            'event_type': event_type,
            'details': details,
            'username': username,
        }
        
        self.security_events.append(event)
        logger.log_security_event(event_type, details, username)
    
    def get_security_events(self, event_type: Optional[str] = None, 
                           username: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get security events, optionally filtered."""
        events = self.security_events
        
        if event_type:
            events = [e for e in events if e['event_type'] == event_type]
        
        if username:
            events = [e for e in events if e['username'] == username]
        
        return events
    
    def detect_suspicious_activity(self, username: str, time_window: int = 3600) -> bool:
        """
        Detect suspicious activity patterns.
        
        Args:
            username: Username to check
            time_window: Time window in seconds to check
            
        Returns:
            True if suspicious activity detected
        """
        current_time = time.time()
        recent_events = [
            e for e in self.security_events
            if e['username'] == username and (current_time - e['timestamp']) <= time_window
        ]
        
        # Check for rapid-fire failed attempts
        failed_attempts = [e for e in recent_events if 'FAILED' in e['event_type']]
        if len(failed_attempts) > 5:
            self.log_security_event('SUSPICIOUS_ACTIVITY', 
                                   f'Multiple failed attempts detected', username)
            return True
        
        # Check for unusual patterns
        unusual_events = [e for e in recent_events if e['event_type'] in [
            'INVALID_SIGNATURE', 'TAMPERING_DETECTED', 'UNAUTHORIZED_ACCESS'
        ]]
        if len(unusual_events) > 2:
            self.log_security_event('SUSPICIOUS_ACTIVITY', 
                                   f'Unusual security events detected', username)
            return True
        
        return False


class SecureFileManager:
    """Secure file operations with additional safety checks."""
    
    @staticmethod
    def secure_write(file_path: str, content: bytes, permissions: int = 0o600) -> None:
        """
        Write file securely with proper permissions.
        
        Args:
            file_path: Path to write to
            content: Content to write
            permissions: File permissions (octal)
        """
        # Validate path
        SecurityValidator.validate_file_path(file_path)
        
        path = Path(file_path)
        
        # Ensure parent directory exists
        path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write file atomically
        temp_path = path.with_suffix(path.suffix + '.tmp')
        
        try:
            with open(temp_path, 'wb') as f:
                f.write(content)
            
            # Set permissions before moving
            os.chmod(temp_path, permissions)
            
            # Atomic move
            temp_path.replace(path)
            
        except Exception as e:
            # Clean up temp file on error
            if temp_path.exists():
                temp_path.unlink()
            raise SecurityError(f"Failed to write file securely: {e}")
    
    @staticmethod
    def secure_read(file_path: str, max_size: Optional[int] = None) -> bytes:
        """
        Read file securely with size validation.
        
        Args:
            file_path: Path to read from
            max_size: Maximum file size to read
            
        Returns:
            File content as bytes
        """
        # Validate path and size
        SecurityValidator.validate_file_path(file_path, max_size)
        
        try:
            with open(file_path, 'rb') as f:
                if max_size:
                    content = f.read(max_size + 1)  # Read one extra byte to check size
                    if len(content) > max_size:
                        raise ValidationError(f"File exceeds maximum size of {max_size} bytes")
                    return content[:-1] if len(content) == max_size + 1 else content
                else:
                    return f.read()
        except IOError as e:
            raise SecurityError(f"Failed to read file securely: {e}")
    
    @staticmethod
    def secure_delete(file_path: str, overwrite_passes: int = 3) -> None:
        """
        Securely delete a file by overwriting it multiple times.
        
        Args:
            file_path: Path to delete
            overwrite_passes: Number of overwrite passes
        """
        path = Path(file_path)
        
        if not path.exists():
            return
        
        try:
            file_size = path.stat().st_size
            
            # Overwrite file multiple times
            with open(path, 'r+b') as f:
                for _ in range(overwrite_passes):
                    f.seek(0)
                    f.write(os.urandom(file_size))
                    f.flush()
                    os.fsync(f.fileno())
            
            # Finally delete the file
            path.unlink()
            
        except Exception as e:
            logger.error(f"Failed to securely delete file {file_path}: {e}")
            # Try regular deletion as fallback
            try:
                path.unlink()
            except Exception:
                pass


# Global security auditor instance
security_auditor = SecurityAuditor()

