"""
CipherChat Logging System
Provides centralized logging functionality with proper security considerations.
"""

import logging
import os
import sys
from pathlib import Path
from typing import Optional
from datetime import datetime

from .config import config


class SecurityLogFormatter(logging.Formatter):
    """Custom formatter that sanitizes sensitive information from logs."""
    
    SENSITIVE_PATTERNS = [
        'private_key',
        'password',
        'secret',
        'token',
        'signature',
        'encrypted_data',
    ]
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record while sanitizing sensitive data."""
        # Create a copy of the record to avoid modifying the original
        record_copy = logging.LogRecord(
            record.name, record.levelno, record.pathname, record.lineno,
            record.msg, record.args, record.exc_info, record.funcName
        )
        
        # Sanitize message
        if isinstance(record_copy.msg, str):
            for pattern in self.SENSITIVE_PATTERNS:
                if pattern in record_copy.msg.lower():
                    # Replace sensitive data with placeholder
                    record_copy.msg = record_copy.msg.replace(
                        record.msg[record.msg.lower().find(pattern):], 
                        f"[{pattern.upper()}_REDACTED]"
                    )
        
        return super().format(record_copy)


class CipherChatLogger:
    """Centralized logging manager for CipherChat."""
    
    def __init__(self, name: str = "cipherchat"):
        self.logger = logging.getLogger(name)
        self._configured = False
        self.setup_logging()
    
    def setup_logging(self) -> None:
        """Setup logging configuration."""
        if self._configured:
            return
        
        # Clear any existing handlers
        self.logger.handlers.clear()
        
        # Set log level
        log_level = getattr(logging, config.log_level.upper(), logging.INFO)
        self.logger.setLevel(log_level)
        
        # Create formatter
        formatter = SecurityLogFormatter(
            fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Console handler
        if config.enable_console_logging:
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setFormatter(formatter)
            console_handler.setLevel(log_level)
            self.logger.addHandler(console_handler)
        
        # File handler
        if config.log_file:
            try:
                # Ensure log directory exists
                log_path = Path(config.log_file)
                log_path.parent.mkdir(parents=True, exist_ok=True)
                
                file_handler = logging.FileHandler(config.log_file)
                file_handler.setFormatter(formatter)
                file_handler.setLevel(log_level)
                self.logger.addHandler(file_handler)
            except Exception as e:
                self.logger.warning(f"Failed to setup file logging: {e}")
        
        # Prevent propagation to avoid duplicate logs
        self.logger.propagate = False
        self._configured = True
    
    def debug(self, message: str, *args, **kwargs) -> None:
        """Log debug message."""
        self.logger.debug(message, *args, **kwargs)
    
    def info(self, message: str, *args, **kwargs) -> None:
        """Log info message."""
        self.logger.info(message, *args, **kwargs)
    
    def warning(self, message: str, *args, **kwargs) -> None:
        """Log warning message."""
        self.logger.warning(message, *args, **kwargs)
    
    def error(self, message: str, *args, **kwargs) -> None:
        """Log error message."""
        self.logger.error(message, *args, **kwargs)
    
    def critical(self, message: str, *args, **kwargs) -> None:
        """Log critical message."""
        self.logger.critical(message, *args, **kwargs)
    
    def log_security_event(self, event_type: str, details: str, username: str = None) -> None:
        """Log security-related events."""
        user_info = f" (User: {username})" if username else ""
        self.logger.warning(f"SECURITY EVENT - {event_type}: {details}{user_info}")
    
    def log_crypto_operation(self, operation: str, username: str = None, success: bool = True) -> None:
        """Log cryptographic operations."""
        status = "SUCCESS" if success else "FAILED"
        user_info = f" (User: {username})" if username else ""
        self.logger.info(f"CRYPTO - {operation}: {status}{user_info}")
    
    def log_performance(self, operation: str, duration_ms: float, details: str = "") -> None:
        """Log performance metrics."""
        if config.enable_performance_metrics:
            self.logger.info(f"PERFORMANCE - {operation}: {duration_ms:.2f}ms {details}")


# Global logger instance
logger = CipherChatLogger()
