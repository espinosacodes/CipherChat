"""
Django admin configuration for chat models.
"""
from django.contrib import admin
from .models import UserProfile, PublicKey, Message, KeyExchange, SecurityLog


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'key_created_at', 'last_activity')
    list_filter = ('key_created_at', 'last_activity')
    search_fields = ('user__username', 'user__email')
    readonly_fields = ('key_created_at', 'last_activity')
    
    fieldsets = (
        ('User Information', {
            'fields': ('user',)
        }),
        ('Cryptographic Keys', {
            'fields': ('public_key', 'private_key', 'key_created_at'),
            'classes': ('collapse',)
        }),
        ('Activity', {
            'fields': ('last_activity',),
            'classes': ('collapse',)
        }),
    )


@admin.register(PublicKey)
class PublicKeyAdmin(admin.ModelAdmin):
    list_display = ('owner', 'key_owner_username', 'imported_at', 'is_active')
    list_filter = ('imported_at', 'is_active')
    search_fields = ('owner__username', 'key_owner_username')
    readonly_fields = ('imported_at',)
    
    fieldsets = (
        ('Key Information', {
            'fields': ('owner', 'key_owner_username', 'is_active')
        }),
        ('Public Key Data', {
            'fields': ('public_key',),
            'classes': ('collapse',)
        }),
        ('Metadata', {
            'fields': ('imported_at',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'message_type', 'created_at', 'read_at')
    list_filter = ('message_type', 'created_at', 'read_at')
    search_fields = ('sender__username', 'recipient__username')
    readonly_fields = ('created_at',)
    
    fieldsets = (
        ('Message Information', {
            'fields': ('sender', 'recipient', 'message_type', 'created_at', 'read_at')
        }),
        ('Encrypted Content', {
            'fields': ('encrypted_content', 'encrypted_aes_key', 'iv', 'signature'),
            'classes': ('collapse',)
        }),
        ('File Information', {
            'fields': ('file_name', 'file_size'),
            'classes': ('collapse',)
        }),
    )


@admin.register(KeyExchange)
class KeyExchangeAdmin(admin.ModelAdmin):
    list_display = ('initiator', 'recipient', 'exchange_type', 'initiated_at', 'completed_at')
    list_filter = ('exchange_type', 'initiated_at', 'completed_at')
    search_fields = ('initiator__username', 'recipient__username')
    readonly_fields = ('initiated_at',)
    
    fieldsets = (
        ('Exchange Information', {
            'fields': ('initiator', 'recipient', 'exchange_type')
        }),
        ('Timing', {
            'fields': ('initiated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
        ('Notes', {
            'fields': ('notes',),
            'classes': ('collapse',)
        }),
    )


@admin.register(SecurityLog)
class SecurityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'operation', 'log_level', 'timestamp', 'success')
    list_filter = ('operation', 'log_level', 'success', 'timestamp')
    search_fields = ('user__username', 'message')
    readonly_fields = ('timestamp',)
    
    fieldsets = (
        ('Event Information', {
            'fields': ('user', 'operation', 'log_level', 'message', 'success')
        }),
        ('Request Details', {
            'fields': ('ip_address', 'user_agent'),
            'classes': ('collapse',)
        }),
        ('Timing', {
            'fields': ('timestamp',),
            'classes': ('collapse',)
        }),
        ('Additional Details', {
            'fields': ('details',),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        """Prevent manual addition of security logs."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Prevent modification of security logs."""
        return False

