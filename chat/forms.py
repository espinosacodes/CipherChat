"""
Django forms for CipherChat application.
"""
from django import forms
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.conf import settings
from .models import Message, PublicKey


class SendMessageForm(forms.ModelForm):
    """Form for sending encrypted messages."""
    recipient_username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter recipient username'
        }),
        help_text="Username of the person you want to send a message to"
    )
    
    message_content = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Type your message here...'
        }),
        validators=[MaxLengthValidator(settings.CIPHERCHAT_MAX_MESSAGE_LENGTH)],
        help_text=f"Maximum {settings.CIPHERCHAT_MAX_MESSAGE_LENGTH} characters"
    )
    
    class Meta:
        model = Message
        fields = ['message_type']
        widgets = {
            'message_type': forms.Select(attrs={'class': 'form-select'})
        }
    
    def clean_recipient_username(self):
        """Validate that the recipient username exists."""
        username = self.cleaned_data['recipient_username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("User with this username does not exist.")
        return username
    
    def clean_message_content(self):
        """Validate message content."""
        content = self.cleaned_data['message_content']
        if not content.strip():
            raise forms.ValidationError("Message content cannot be empty.")
        return content


class ImportPublicKeyForm(forms.ModelForm):
    """Form for importing public keys from other users."""
    key_owner_username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username of the key owner'
        }),
        help_text="Username of the person whose public key you want to import"
    )
    
    public_key = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 10,
            'placeholder': 'Paste the public key here (PEM format)'
        }),
        help_text="Paste the public key in PEM format"
    )
    
    class Meta:
        model = PublicKey
        fields = ['key_owner_username', 'public_key']
    
    def clean_public_key(self):
        """Validate that the public key is in valid PEM format."""
        key = self.cleaned_data['public_key']
        if not key.strip().startswith('-----BEGIN PUBLIC KEY-----'):
            raise forms.ValidationError("Invalid public key format. Please provide a valid PEM-encoded public key.")
        if not key.strip().endswith('-----END PUBLIC KEY-----'):
            raise forms.ValidationError("Invalid public key format. Please provide a valid PEM-encoded public key.")
        return key
    
    def clean_key_owner_username(self):
        """Validate that the key owner username exists."""
        username = self.cleaned_data['key_owner_username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("User with this username does not exist.")
        return username


class KeyExchangeForm(forms.Form):
    """Form for initiating key exchanges."""
    recipient_username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter recipient username'
        }),
        help_text="Username of the person you want to exchange keys with"
    )
    
    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Optional notes about this key exchange'
        }),
        help_text="Optional notes about this key exchange"
    )
    
    def clean_recipient_username(self):
        """Validate that the recipient username exists."""
        username = self.cleaned_data['recipient_username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("User with this username does not exist.")
        return username


class SearchMessagesForm(forms.Form):
    """Form for searching through messages."""
    SEARCH_OPTIONS = [
        ('all', 'All Messages'),
        ('sent', 'Sent Messages'),
        ('received', 'Received Messages'),
        ('unread', 'Unread Messages'),
    ]
    
    search_query = forms.CharField(
        required=False,
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search messages...'
        }),
        help_text="Search through message content (will search encrypted content)"
    )
    
    message_type = forms.ChoiceField(
        choices=[('', 'All Types')] + Message.MESSAGE_TYPES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    date_from = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        help_text="Search messages from this date"
    )
    
    date_to = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        }),
        help_text="Search messages until this date"
    )
    
    search_scope = forms.ChoiceField(
        choices=SEARCH_OPTIONS,
        initial='all',
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class FileUploadForm(forms.Form):
    """Form for uploading encrypted files."""
    recipient_username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter recipient username'
        }),
        help_text="Username of the person you want to send the file to"
    )
    
    file = forms.FileField(
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '*/*'
        }),
        help_text="Select a file to encrypt and send"
    )
    
    message = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Optional message to accompany the file'
        }),
        help_text="Optional message to send with the file"
    )
    
    def clean_file(self):
        """Validate the uploaded file."""
        file = self.cleaned_data['file']
        if file.size > settings.FILE_UPLOAD_MAX_MEMORY_SIZE:
            raise forms.ValidationError(f"File size must be under {settings.FILE_UPLOAD_MAX_MEMORY_SIZE // (1024*1024)}MB.")
        return file
    
    def clean_recipient_username(self):
        """Validate that the recipient username exists."""
        username = self.cleaned_data['recipient_username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("User with this username does not exist.")
        return username

