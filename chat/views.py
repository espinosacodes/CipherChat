"""
Django views for CipherChat application.
"""
import json
import base64
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

from .models import Message, PublicKey, KeyExchange, SecurityLog, UserProfile
from .forms import (
    SendMessageForm, ImportPublicKeyForm, KeyExchangeForm, 
    SearchMessagesForm, FileUploadForm
)

# TODO: Import the existing crypto engine when ready
# import sys
# import os
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
# from crypto_engine import CryptoEngine
# from key_manager import KeyManager
# from secure_channel import SecureChannel

def log_security_event(operation, message, user=None, success=True, details=None):
    """Log security events for auditing."""
    try:
        SecurityLog.objects.create(
            operation=operation,
            message=message,
            user=user,
            success=success,
            details=details or {}
        )
    except Exception as e:
        # Fallback logging if database logging fails
        print(f"Security log error: {e}")

@login_required
def dashboard(request):
    """Main dashboard view."""
    try:
        # Get user's recent messages
        recent_messages = Message.objects.filter(
            Q(sender=request.user) | Q(recipient=request.user)
        ).order_by('-created_at')[:5]
        
        # Get unread message count
        unread_count = Message.objects.filter(
            recipient=request.user,
            read_at__isnull=True
        ).count()
        
        # Get imported keys count
        imported_keys = PublicKey.objects.filter(owner=request.user).count()
        
        # Check if user has generated keys
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            has_keys = bool(user_profile.public_key and user_profile.private_key)
        except UserProfile.DoesNotExist:
            has_keys = False
        
        # Get additional statistics
        total_messages = Message.objects.filter(
            Q(sender=request.user) | Q(recipient=request.user)
        ).count()
        
        messages_sent = Message.objects.filter(sender=request.user).count()
        messages_received = Message.objects.filter(recipient=request.user).count()
        
        # Get recent security logs for activity feed
        recent_activities = SecurityLog.objects.filter(
            user=request.user
        ).order_by('-timestamp')[:5]
        
        # Calculate security score (placeholder)
        security_score = 85  # Placeholder value
        
        # Get keys generated count
        keys_generated = PublicKey.objects.filter(owner=request.user).count()
        
        context = {
            'recent_messages': recent_messages,
            'unread_count': unread_count,
            'imported_keys': imported_keys,
            'has_keys': has_keys,
            'total_messages': total_messages,
            'total_keys': imported_keys,
            'security_score': security_score,
            'recent_activities': recent_activities,
            'messages_sent': messages_sent,
            'messages_received': messages_received,
            'keys_generated': keys_generated,
        }
        
        return render(request, 'chat/dashboard.html', context)
        
    except Exception as e:
        messages.error(request, f"Error loading dashboard: {str(e)}")
        return render(request, 'chat/dashboard.html', {})

@login_required
def send_message(request):
    """Send encrypted message view."""
    if request.method == 'POST':
        form = SendMessageForm(request.POST)
        if form.is_valid():
            try:
                recipient_username = form.cleaned_data['recipient_username']
                message_content = form.cleaned_data['message_content']
                message_type = form.cleaned_data['message_type']
                
                # Check if recipient exists
                try:
                    recipient = User.objects.get(username=recipient_username)
                except User.DoesNotExist:
                    messages.error(request, f"User '{recipient_username}' not found.")
                    return render(request, 'chat/send_message.html', {'form': form})
                
                # Check if sender has keys
                try:
                    sender_profile = UserProfile.objects.get(user=request.user)
                    if not sender_profile.public_key or not sender_profile.private_key:
                        messages.error(request, "You need to generate cryptographic keys first.")
                        return render(request, 'chat/send_message.html', {'form': form})
                except UserProfile.DoesNotExist:
                    messages.error(request, "You need to generate cryptographic keys first.")
                    return render(request, 'chat/send_message.html', {'form': form})
                
                # Check if recipient has keys
                try:
                    recipient_profile = UserProfile.objects.get(user=recipient)
                    if not recipient_profile.public_key:
                        messages.error(request, f"User '{recipient_username}' has not generated keys yet.")
                        return render(request, 'chat/send_message.html', {'form': form})
                except UserProfile.DoesNotExist:
                    messages.error(request, f"User '{recipient_username}' has not generated keys yet.")
                    return render(request, 'chat/send_message.html', {'form': form})
                
                # TODO: Implement actual encryption when crypto engine is ready
                # For now, create a placeholder encrypted message
                encrypted_content = f"ENCRYPTED:{message_content}"
                aes_key = "placeholder_aes_key"
                iv = "placeholder_iv"
                signature = "placeholder_signature"
                
                # Create the message
                message = Message.objects.create(
                    sender=request.user,
                    recipient=recipient,
                    encrypted_content=encrypted_content,
                    message_type=message_type,
                    encrypted_aes_key=aes_key,
                    iv=iv,
                    signature=signature
                )
                
                # Log the event
                log_security_event(
                    "message_send",
                    f"Message sent to {recipient_username}",
                    request.user,
                    success=True,
                    details={'message_id': message.id, 'recipient': recipient_username}
                )
                
                messages.success(request, f"Message sent successfully to {recipient_username}!")
                return redirect('chat:dashboard')
                
            except Exception as e:
                messages.error(request, f"Error sending message: {str(e)}")
                log_security_event(
                    "message_send",
                    f"Failed to send message: {str(e)}",
                    request.user,
                    success=False,
                    details={'error': str(e)}
                )
    else:
        form = SendMessageForm()
    
    return render(request, 'chat/send_message.html', {'form': form})

@login_required
def view_messages(request):
    """View all messages for the current user."""
    try:
        # Get search parameters
        search_query = request.GET.get('search', '')
        message_type = request.GET.get('message_type', '')
        sender_filter = request.GET.get('sender', '')
        
        # Base queryset
        messages_qs = Message.objects.filter(
            Q(sender=request.user) | Q(recipient=request.user)
        )
        
        # Apply filters
        if search_query:
            messages_qs = messages_qs.filter(encrypted_content__icontains=search_query)
        if message_type:
            messages_qs = messages_qs.filter(message_type=message_type)
        if sender_filter:
            messages_qs = messages_qs.filter(sender__username__icontains=sender_filter)
        
        # Order by created_at
        messages_qs = messages_qs.order_by('-created_at')
        
        # Pagination
        paginator = Paginator(messages_qs, 20)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Get all users for sender filter dropdown
        all_users = User.objects.exclude(id=request.user.id).order_by('username')
        
        context = {
            'page_obj': page_obj,
            'search_query': search_query,
            'message_type': message_type,
            'sender_filter': sender_filter,
            'all_users': all_users,
        }
        
        return render(request, 'chat/view_messages.html', context)
        
    except Exception as e:
        messages.error(request, f"Error loading messages: {str(e)}")
        return render(request, 'chat/view_messages.html', {})

@login_required
def decrypt_message(request, message_id):
    """Decrypt and view a specific message."""
    try:
        message = get_object_or_404(Message, id=message_id)
        
        # Check if user is sender or recipient
        if message.sender != request.user and message.recipient != request.user:
            messages.error(request, "You don't have permission to view this message.")
            return redirect('chat:view_messages')
        
        # TODO: Implement actual decryption when crypto engine is ready
        # For now, show the encrypted content
        decrypted_content = message.encrypted_content.replace("ENCRYPTED:", "")
        
        # Mark as read if user is recipient
        if message.recipient == request.user and not message.read_at:
            message.read_at = timezone.now()
            message.save()
        
        context = {
            'message': message,
            'decrypted_content': decrypted_content,
        }
        
        return render(request, 'chat/decrypt_message.html', context)
        
    except Exception as e:
        messages.error(request, f"Error decrypting message: {str(e)}")
        return redirect('chat:view_messages')

@login_required
def import_key(request):
    """Import public key from another user."""
    if request.method == 'POST':
        form = ImportPublicKeyForm(request.POST)
        if form.is_valid():
            try:
                username = form.cleaned_data['key_owner_username']
                public_key_data = form.cleaned_data['public_key']
                
                # Check if user exists
                try:
                    user = User.objects.get(username=username)
                except User.DoesNotExist:
                    messages.error(request, f"User '{username}' not found.")
                    return render(request, 'chat/import_key.html', {'form': form})
                
                # Check if key already exists
                if PublicKey.objects.filter(owner=request.user, key_owner_username=username).exists():
                    messages.warning(request, f"Public key for '{username}' already imported.")
                    return redirect('chat:manage_keys')
                
                # TODO: Validate public key format when crypto engine is ready
                # For now, accept any key data
                
                # Create the public key record
                public_key = PublicKey.objects.create(
                    owner=request.user,
                    key_owner_username=username,
                    public_key=public_key_data
                )
                
                # Log the event
                log_security_event(
                    "key_import",
                    f"Public key imported for user {username}",
                    request.user,
                    success=True,
                    details={'username': username, 'key_id': public_key.id}
                )
                
                messages.success(request, f"Public key for '{username}' imported successfully!")
                return redirect('chat:manage_keys')
                
            except Exception as e:
                messages.error(request, f"Error importing key: {str(e)}")
                log_security_event(
                    "key_imported",
                    f"Failed to import key: {str(e)}",
                    request.user,
                    success=False,
                    details={'error': str(e)}
                )
    else:
        form = ImportPublicKeyForm()
    
    return render(request, 'chat/import_key.html', {'form': form})

@login_required
def manage_keys(request):
    """Manage cryptographic keys."""
    try:
        # Get user's profile
        try:
            user_profile = UserProfile.objects.get(user=request.user)
            has_keys = bool(user_profile.public_key and user_profile.private_key)
        except UserProfile.DoesNotExist:
            has_keys = False
            user_profile = None
        
        # Get imported public keys
        imported_keys = PublicKey.objects.filter(owner=request.user)
        
        context = {
            'user_profile': user_profile,
            'has_keys': has_keys,
            'imported_keys': imported_keys,
        }
        
        return render(request, 'chat/manage_keys.html', context)
        
    except Exception as e:
        messages.error(request, f"Error loading keys: {str(e)}")
        return render(request, 'chat/manage_keys.html', {})

@login_required
def generate_keys(request):
    """Generate new cryptographic keys for the user."""
    try:
        # TODO: Implement actual key generation when crypto engine is ready
        # For now, create placeholder keys
        
        # Create or get user profile
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)
        
        # Generate placeholder keys (replace with actual crypto engine)
        placeholder_public_key = "-----BEGIN PUBLIC KEY-----\nPLACEHOLDER_PUBLIC_KEY\n-----END PUBLIC KEY-----"
        placeholder_private_key = "-----BEGIN PRIVATE KEY-----\nPLACEHOLDER_PRIVATE_KEY\n-----END PRIVATE KEY-----"
        
        # Update profile
        user_profile.public_key = placeholder_public_key
        user_profile.private_key = placeholder_private_key
        user_profile.key_created_at = timezone.now()
        user_profile.save()
        
        # Log the event
        log_security_event(
            "key_generation",
            "New cryptographic keys generated",
            request.user,
            success=True,
            details={'key_size': 2048}
        )
        
        messages.success(request, "Cryptographic keys generated successfully!")
        return redirect('chat:manage_keys')
        
    except Exception as e:
        messages.error(request, f"Error generating keys: {str(e)}")
        log_security_event(
            "key_generation",
            f"Failed to generate keys: {str(e)}",
            request.user,
            success=False,
            details={'error': str(e)}
        )
        return redirect('chat:manage_keys')

@login_required
def export_public_key(request):
    """Export user's public key."""
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        
        if not user_profile.public_key:
            messages.error(request, "You haven't generated any keys yet.")
            return redirect('chat:manage_keys')
        
        # Create response with public key
        response = HttpResponse(user_profile.public_key, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename="{request.user.username}_public_key.pem"'
        
        # Log the event
        log_security_event(
            "key_generation",
            "Public key exported",
            request.user,
            success=True
        )
        
        return response
        
    except UserProfile.DoesNotExist:
        messages.error(request, "You haven't generated any keys yet.")
        return redirect('chat:manage_keys')
    except Exception as e:
        messages.error(request, f"Error exporting key: {str(e)}")
        return redirect('chat:manage_keys')

@login_required
def key_exchange(request):
    """Initiate key exchange with another user."""
    if request.method == 'POST':
        form = KeyExchangeForm(request.POST)
        if form.is_valid():
            try:
                recipient_username = form.cleaned_data['recipient']
                exchange_type = form.cleaned_data['exchange_type']
                
                # Check if recipient exists
                try:
                    recipient = User.objects.get(username=recipient_username)
                except User.DoesNotExist:
                    messages.error(request, f"User '{recipient_username}' not found.")
                    return render(request, 'chat/key_exchange.html', {'form': form})
                
                # TODO: Implement actual key exchange when crypto engine is ready
                # For now, create a placeholder exchange record
                
                exchange = KeyExchange.objects.create(
                    initiator=request.user,
                    recipient=recipient,
                    exchange_type=exchange_type,
                    notes='Key exchange initiated'
                )
                
                # Log the event
                log_security_event(
                    "key_exchange",
                    f"Key exchange initiated with {recipient_username}",
                    request.user,
                    success=True,
                    details={'recipient': recipient_username, 'type': exchange_type}
                )
                
                messages.success(request, f"Key exchange initiated with {recipient_username}!")
                return redirect('chat:manage_keys')
                
            except Exception as e:
                messages.error(request, f"Error initiating key exchange: {str(e)}")
                return render(request, 'chat/key_exchange.html', {'form': form})
    else:
        form = KeyExchangeForm()
    
    return render(request, 'chat/key_exchange.html', {'form': form})

@login_required
def security_logs(request):
    """View security logs for the current user."""
    try:
        # Get user's security logs
        logs = SecurityLog.objects.filter(user=request.user).order_by('-timestamp')
        
        # Pagination
        paginator = Paginator(logs, 50)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'page_obj': page_obj,
        }
        
        return render(request, 'chat/security_logs.html', context)
        
    except Exception as e:
        messages.error(request, f"Error loading security logs: {str(e)}")
        return render(request, 'chat/security_logs.html', {})


@login_required
def security_overview(request):
    """Display comprehensive security overview page."""
    return render(request, 'chat/security.html')


@login_required
def get_key_details(request, key_id):
    """Get details for a specific imported public key via AJAX."""
    try:
        # Get the key, ensuring it belongs to the current user
        key = get_object_or_404(PublicKey, id=key_id, owner=request.user)
        
        # Format the key data for display
        key_data = {
            'id': key.id,
            'key_owner_username': key.key_owner_username,
            'public_key': key.public_key,
            'imported_at': key.imported_at.strftime('%B %d, %Y at %H:%M'),
            'is_active': key.is_active,
            'owner': key.owner.username,
        }
        
        # Log the event
        log_security_event(
            "key_import",
            f"Viewed details for key from {key.key_owner_username}",
            request.user,
            success=True,
            details={'key_id': key.id, 'key_owner': key.key_owner_username}
        )
        
        return JsonResponse({
            'success': True,
            'key': key_data
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
