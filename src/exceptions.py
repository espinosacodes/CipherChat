"""
CipherChat Custom Exceptions
Defines custom exception classes for better error handling.
"""


class CipherChatError(Exception):
    """Base exception class for CipherChat."""
    
    def __init__(self, message: str, error_code: str = None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code or "GENERAL_ERROR"


class CryptographicError(CipherChatError):
    """Raised when cryptographic operations fail."""
    
    def __init__(self, message: str, operation: str = None):
        super().__init__(message, "CRYPTO_ERROR")
        self.operation = operation


class KeyManagementError(CipherChatError):
    """Raised when key management operations fail."""
    
    def __init__(self, message: str, username: str = None):
        super().__init__(message, "KEY_ERROR")
        self.username = username


class MessageError(CipherChatError):
    """Raised when message processing fails."""
    
    def __init__(self, message: str, message_type: str = None):
        super().__init__(message, "MESSAGE_ERROR")
        self.message_type = message_type


class AuthenticationError(CipherChatError):
    """Raised when authentication fails."""
    
    def __init__(self, message: str, username: str = None):
        super().__init__(message, "AUTH_ERROR")
        self.username = username


class ValidationError(CipherChatError):
    """Raised when input validation fails."""
    
    def __init__(self, message: str, field: str = None):
        super().__init__(message, "VALIDATION_ERROR")
        self.field = field


class ConfigurationError(CipherChatError):
    """Raised when configuration is invalid."""
    
    def __init__(self, message: str, setting: str = None):
        super().__init__(message, "CONFIG_ERROR")
        self.setting = setting


class NetworkError(CipherChatError):
    """Raised when network operations fail."""
    
    def __init__(self, message: str, endpoint: str = None):
        super().__init__(message, "NETWORK_ERROR")
        self.endpoint = endpoint


class SecurityError(CipherChatError):
    """Raised when security violations are detected."""
    
    def __init__(self, message: str, security_event: str = None):
        super().__init__(message, "SECURITY_ERROR")
        self.security_event = security_event
