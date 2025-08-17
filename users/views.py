"""
Django views for user management.
"""
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, update_session_auth_hash, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm, 
    UserProfileForm, ChangePasswordForm
)


def register(request):
    """User registration view."""
    if request.user.is_authenticated:
        return redirect('chat:dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                
                # Log the user in automatically
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                
                messages.success(request, f"Welcome to CipherChat, {username}! Your account has been created successfully.")
                return redirect('chat:dashboard')
                
            except Exception as e:
                messages.error(request, f"Error creating account: {str(e)}")
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    """User login view."""
    if request.user.is_authenticated:
        return redirect('chat:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # Handle remember me functionality
                if not form.cleaned_data.get('remember_me'):
                    request.session.set_expiry(0)
                
                # Log the login event
                try:
                    from chat.models import SecurityLog
                    SecurityLog.objects.create(
                        user=user,
                        operation='login',
                        log_level='info',
                        message=f'User {username} logged in successfully',
                        ip_address=request.META.get('REMOTE_ADDR'),
                        user_agent=request.META.get('HTTP_USER_AGENT', ''),
                        success=True
                    )
                except Exception as e:
                    # If logging fails, continue with login
                    pass
                
                messages.success(request, f"Welcome back, {username}!")
                return redirect('chat:dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})


@login_required
def profile(request):
    """User profile view."""
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=request.user)
        password_form = ChangePasswordForm(request.POST)
        
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('users:profile')
        
        if password_form.is_valid():
            # Verify current password
            if not request.user.check_password(password_form.cleaned_data['current_password']):
                messages.error(request, "Current password is incorrect.")
                return redirect('users:profile')
            
            # Change password
            try:
                request.user.set_password(password_form.cleaned_data['new_password1'])
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, "Password changed successfully!")
                return redirect('users:profile')
            except Exception as e:
                messages.error(request, f"Error changing password: {str(e)}")
    else:
        profile_form = UserProfileForm(instance=request.user)
        password_form = ChangePasswordForm()
    
    context = {
        'profile_form': profile_form,
        'password_form': password_form,
    }
    
    return render(request, 'users/profile.html', context)


@login_required
def delete_account(request):
    """Delete user account view."""
    if request.method == 'POST':
        try:
            # Delete the user (this will cascade to related objects)
            username = request.user.username
            request.user.delete()
            messages.success(request, f"Account '{username}' has been deleted successfully.")
            return redirect('users:login')
        except Exception as e:
            messages.error(request, f"Error deleting account: {str(e)}")
    
    return render(request, 'users/delete_account.html')


def user_logout(request):
    """Custom user logout view."""
    from django.utils import timezone
    
    if request.user.is_authenticated:
        username = request.user.username
        
        # Log the logout event before logging out
        try:
            from chat.models import SecurityLog
            SecurityLog.objects.create(
                user=request.user,
                operation='logout',
                log_level='info',
                message=f'User {username} logged out successfully',
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                success=True
            )
        except Exception as e:
            # If logging fails, continue with logout
            pass
        
        logout(request)
        messages.success(request, f"Goodbye, {username}! You have been successfully logged out.")
    else:
        messages.info(request, "You are not currently logged in.")
    
    context = {
        'now': timezone.now(),
    }
    
    return render(request, 'users/logout.html', context)

