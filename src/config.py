"""
CipherChat Configuration Management
Handles application configuration and environment variables.
"""

import os
from pathlib import Path
from typing import Any, Dict, Optional
from dataclasses import dataclass


@dataclass
class CipherChatConfig:
    """Configuration settings for CipherChat."""
    
    # Cryptographic settings
    rsa_key_size: int = 2048
    aes_key_size: int = 32  # 256 bits
    signature_salt_length: int = 32
    
    # Directory settings
    keys_directory: str = "keys"
    messages_directory: str = "messages"
    temp_directory: str = "temp"
    
    # Security settings
    max_message_size: int = 1024 * 1024  # 1MB
    session_timeout: int = 3600  # 1 hour
    enable_key_rotation: bool = True
    
    # Logging settings
    log_level: str = "INFO"
    log_file: Optional[str] = None
    enable_console_logging: bool = True
    
    # Performance settings
    enable_performance_metrics: bool = False
    cache_public_keys: bool = True
    
    @classmethod
    def from_env(cls) -> 'CipherChatConfig':
        """Create configuration from environment variables."""
        return cls(
            rsa_key_size=int(os.getenv('CIPHERCHAT_RSA_KEY_SIZE', '2048')),
            aes_key_size=int(os.getenv('CIPHERCHAT_AES_KEY_SIZE', '32')),
            keys_directory=os.getenv('CIPHERCHAT_KEYS_DIR', 'keys'),
            messages_directory=os.getenv('CIPHERCHAT_MESSAGES_DIR', 'messages'),
            temp_directory=os.getenv('CIPHERCHAT_TEMP_DIR', 'temp'),
            max_message_size=int(os.getenv('CIPHERCHAT_MAX_MESSAGE_SIZE', str(1024 * 1024))),
            session_timeout=int(os.getenv('CIPHERCHAT_SESSION_TIMEOUT', '3600')),
            enable_key_rotation=os.getenv('CIPHERCHAT_ENABLE_KEY_ROTATION', 'True').lower() == 'true',
            log_level=os.getenv('CIPHERCHAT_LOG_LEVEL', 'INFO'),
            log_file=os.getenv('CIPHERCHAT_LOG_FILE'),
            enable_console_logging=os.getenv('CIPHERCHAT_ENABLE_CONSOLE_LOGGING', 'True').lower() == 'true',
            enable_performance_metrics=os.getenv('CIPHERCHAT_ENABLE_PERFORMANCE_METRICS', 'False').lower() == 'true',
            cache_public_keys=os.getenv('CIPHERCHAT_CACHE_PUBLIC_KEYS', 'True').lower() == 'true',
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            'rsa_key_size': self.rsa_key_size,
            'aes_key_size': self.aes_key_size,
            'keys_directory': self.keys_directory,
            'messages_directory': self.messages_directory,
            'temp_directory': self.temp_directory,
            'max_message_size': self.max_message_size,
            'session_timeout': self.session_timeout,
            'enable_key_rotation': self.enable_key_rotation,
            'log_level': self.log_level,
            'log_file': self.log_file,
            'enable_console_logging': self.enable_console_logging,
            'enable_performance_metrics': self.enable_performance_metrics,
            'cache_public_keys': self.cache_public_keys,
        }
    
    def validate(self) -> bool:
        """Validate configuration settings."""
        if self.rsa_key_size < 2048:
            raise ValueError("RSA key size must be at least 2048 bits for security")
        
        if self.aes_key_size not in [16, 24, 32]:
            raise ValueError("AES key size must be 16, 24, or 32 bytes")
        
        if self.max_message_size <= 0:
            raise ValueError("Maximum message size must be positive")
        
        if self.session_timeout <= 0:
            raise ValueError("Session timeout must be positive")
        
        return True
    
    def ensure_directories(self) -> None:
        """Ensure all required directories exist."""
        dirs = [
            self.keys_directory,
            self.messages_directory,
            self.temp_directory,
            os.path.join(self.keys_directory, "imported"),
        ]
        
        for directory in dirs:
            Path(directory).mkdir(parents=True, exist_ok=True)


# Global configuration instance
config = CipherChatConfig.from_env()
