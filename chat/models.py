"""
Django models for CipherChat application.
"""
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.conf import settings
import os


class UserProfile(models.Model):
    """Extended user profile for CipherChat."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    public_key = models.TextField(blank=True, help_text="User's public RSA key")
    private_key = models.TextField(blank=True, help_text="User's encrypted private RSA key")
    key_created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    class Meta:
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"


class PublicKey(models.Model):
    """Imported public keys from other users."""
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='imported_keys')
    key_owner_username = models.CharField(max_length=150, help_text="Username of the key owner")
    public_key = models.TextField(help_text="Imported public RSA key")
    imported_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, help_text="Whether this key is currently active")
    
    def __str__(self):
        return f"{self.key_owner_username}'s key imported by {self.owner.username}"
    
    class Meta:
        verbose_name = "Public Key"
        verbose_name_plural = "Public Keys"
        unique_together = ['owner', 'key_owner_username']


class Message(models.Model):
    """Messages between users (encrypted or non-encrypted)."""
    MESSAGE_TYPES = [
        ('text', 'Text Message'),
        ('file', 'File Attachment'),
        ('key_exchange', 'Key Exchange'),
    ]
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='text')
    
    # Message content (encrypted or plaintext)
    encrypted_content = models.TextField(help_text="Message content (encrypted or plaintext)")
    is_encrypted = models.BooleanField(default=True, help_text="Whether this message is encrypted")
    
    # Encryption-related fields (optional for non-encrypted messages)
    encrypted_aes_key = models.TextField(blank=True, null=True, help_text="RSA encrypted AES key")
    iv = models.TextField(blank=True, null=True, help_text="Initialization vector for AES encryption")
    signature = models.TextField(blank=True, null=True, help_text="Digital signature for message verification")
    
    # Message metadata
    created_at = models.DateTimeField(auto_now_add=True)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # File attachment fields (if applicable)
    file_name = models.CharField(max_length=255, blank=True, help_text="Original filename if file attachment")
    file_size = models.IntegerField(null=True, blank=True, help_text="File size in bytes")
    
    def __str__(self):
        encryption_status = "ENCRYPTED" if self.is_encrypted else "PLAINTEXT"
        return f"{encryption_status} Message from {self.sender.username} to {self.recipient.username} ({self.created_at})"
    
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"
        ordering = ['-created_at']


class KeyExchange(models.Model):
    """Records of key exchange operations."""
    EXCHANGE_TYPES = [
        ('initiated', 'Initiated'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    initiator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='initiated_exchanges')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_exchanges')
    exchange_type = models.CharField(max_length=20, choices=EXCHANGE_TYPES, default='initiated')
    initiated_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True, help_text="Additional notes about the exchange")
    
    def __str__(self):
        return f"Key exchange: {self.initiator.username} → {self.recipient.username}"
    
    class Meta:
        verbose_name = "Key Exchange"
        verbose_name_plural = "Key Exchanges"
        ordering = ['-initiated_at']


class SecurityLog(models.Model):
    """Security-related events and operations."""
    LOG_LEVELS = [
        ('info', 'Information'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('critical', 'Critical'),
    ]
    
    OPERATION_TYPES = [
        ('key_generation', 'Key Generation'),
        ('key_import', 'Key Import'),
        ('message_send', 'Message Send'),
        ('message_receive', 'Message Receive'),
        ('key_exchange', 'Key Exchange'),
        ('login', 'User Login'),
        ('logout', 'User Logout'),
        ('security_check', 'Security Check'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='security_logs', null=True, blank=True)
    operation = models.CharField(max_length=50, choices=OPERATION_TYPES)
    log_level = models.CharField(max_length=20, choices=LOG_LEVELS, default='info')
    message = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    success = models.BooleanField(default=True)
    details = models.JSONField(default=dict, blank=True)
    
    def __str__(self):
        return f"{self.operation} - {self.user.username if self.user else 'System'} ({self.timestamp})"
    
    class Meta:
        verbose_name = "Security Log"
        verbose_name_plural = "Security Logs"
        ordering = ['-timestamp']

