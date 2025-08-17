"""
Django management command to initialize test data for CipherChat.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
import os
import json
from datetime import timedelta

from chat.models import UserProfile, PublicKey, Message, KeyExchange, SecurityLog


class Command(BaseCommand):
    help = 'Initialize test data for CipherChat application'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=5,
            help='Number of test users to create (default: 5)'
        )
        parser.add_argument(
            '--messages',
            type=int,
            default=10,
            help='Number of test messages to create (default: 10)'
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before creating new test data'
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            self.clear_existing_data()

        self.stdout.write('Creating test data...')
        
        # Create test users
        users = self.create_test_users(options['users'])
        
        # Generate encryption keys for users
        self.generate_user_keys(users)
        
        # Import public keys between users
        self.import_public_keys(users)
        
        # Create test messages
        self.create_test_messages(users, options['messages'])
        
        # Create key exchanges
        self.create_key_exchanges(users)
        
        # Create security logs
        self.create_security_logs(users)
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created test data:\n'
                f'- {len(users)} users\n'
                f'- {len(users)} user profiles with keys\n'
                f'- {len(users) * (len(users) - 1)} public key imports\n'
                f'- {options["messages"]} encrypted messages\n'
                f'- {len(users) * 2} key exchanges\n'
                f'- {len(users) * 3} security logs'
            )
        )

    def clear_existing_data(self):
        """Clear existing test data."""
        SecurityLog.objects.all().delete()
        KeyExchange.objects.all().delete()
        Message.objects.all().delete()
        PublicKey.objects.all().delete()
        UserProfile.objects.all().delete()
        User.objects.filter(username__startswith='testuser').delete()

    def create_test_users(self, num_users):
        """Create test users."""
        users = []
        test_passwords = ['testpass123', 'secure456', 'password789', 'secret101', 'cipher202']
        
        for i in range(num_users):
            username = f'testuser{i+1}'
            email = f'{username}@example.com'
            password = test_passwords[i % len(test_passwords)]
            
            user, created = User.objects.get_or_create(
                username=username,
                defaults={
                    'email': email,
                    'first_name': f'Test{i+1}',
                    'last_name': 'User',
                    'is_active': True,
                    'date_joined': timezone.now() - timedelta(days=i)
                }
            )
            
            if created:
                user.set_password(password)
                user.save()
                self.stdout.write(f'Created user: {username} (password: {password})')
            else:
                self.stdout.write(f'User already exists: {username}')
            
            users.append(user)
        
        return users

    def generate_user_keys(self, users):
        """Generate RSA key pairs for users."""
        for user in users:
            profile, created = UserProfile.objects.get_or_create(user=user)
            
            if not profile.public_key:  # Only generate if keys don't exist
                # Generate RSA key pair
                private_key = rsa.generate_private_key(
                    public_exponent=65537,
                    key_size=2048,
                    backend=default_backend()
                )
                public_key = private_key.public_key()
                
                # Serialize keys
                public_pem = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
                
                private_pem = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
                
                # Store keys
                profile.public_key = public_pem.decode('utf-8')
                profile.private_key = private_pem.decode('utf-8')
                profile.save()
                
                self.stdout.write(f'Generated keys for: {user.username}')

    def import_public_keys(self, users):
        """Import public keys between users."""
        for user in users:
            user_profile = UserProfile.objects.get(user=user)
            
            for other_user in users:
                if other_user != user:
                    other_profile = UserProfile.objects.get(user=other_user)
                    
                    # Import public key
                    public_key, created = PublicKey.objects.get_or_create(
                        owner=user,
                        key_owner_username=other_user.username,
                        defaults={
                            'public_key': other_profile.public_key,
                            'is_active': True
                        }
                    )
                    
                    if created:
                        self.stdout.write(f'Imported key: {other_user.username} → {user.username}')

    def create_test_messages(self, users, num_messages):
        """Create test encrypted messages."""
        test_messages = [
            "Hello! How are you doing today?",
            "This is a test encrypted message.",
            "The weather is nice today, isn't it?",
            "Did you finish the project we discussed?",
            "Let's meet for coffee tomorrow!",
            "I've been working on some new encryption algorithms.",
            "Have you seen the latest security updates?",
            "The meeting is scheduled for 3 PM.",
            "Thanks for your help with the code review.",
            "Happy birthday! 🎉",
            "Don't forget to backup your keys!",
            "The encryption is working perfectly.",
            "This message is end-to-end encrypted.",
            "Remember to use strong passwords.",
            "Security first, always!"
        ]
        
        for i in range(num_messages):
            sender = users[i % len(users)]
            recipient = users[(i + 1) % len(users)]
            
            # Get sender's private key and recipient's public key
            sender_profile = UserProfile.objects.get(user=sender)
            recipient_public_key = PublicKey.objects.get(
                owner=sender,
                key_owner_username=recipient.username
            )
            
            # Create a test message
            message_content = test_messages[i % len(test_messages)]
            
            # Simulate encryption (in real app, this would be proper encryption)
            encrypted_content = base64.b64encode(message_content.encode()).decode()
            encrypted_aes_key = base64.b64encode(b"simulated_aes_key").decode()
            iv = base64.b64encode(os.urandom(16)).decode()
            signature = base64.b64encode(b"simulated_signature").decode()
            
            # Create message
            message = Message.objects.create(
                sender=sender,
                recipient=recipient,
                message_type='text',
                encrypted_content=encrypted_content,
                encrypted_aes_key=encrypted_aes_key,
                iv=iv,
                signature=signature,
                created_at=timezone.now() - timedelta(hours=i)
            )
            
            if i < 5:  # Mark first 5 messages as read
                message.read_at = timezone.now() - timedelta(minutes=i*10)
                message.save()

    def create_key_exchanges(self, users):
        """Create test key exchanges."""
        for i, user in enumerate(users):
            recipient = users[(i + 1) % len(users)]
            
            # Create initiated exchange
            KeyExchange.objects.create(
                initiator=user,
                recipient=recipient,
                exchange_type='initiated',
                notes=f'Test key exchange initiated by {user.username}'
            )
            
            # Create completed exchange
            completed_exchange = KeyExchange.objects.create(
                initiator=user,
                recipient=recipient,
                exchange_type='completed',
                completed_at=timezone.now() - timedelta(hours=i),
                notes=f'Test key exchange completed between {user.username} and {recipient.username}'
            )

    def create_security_logs(self, users):
        """Create test security logs."""
        operations = ['login', 'logout', 'key_generation', 'message_send', 'message_receive']
        log_levels = ['info', 'warning', 'error']
        
        for user in users:
            for i, operation in enumerate(operations):
                SecurityLog.objects.create(
                    user=user,
                    operation=operation,
                    log_level=log_levels[i % len(log_levels)],
                    message=f'Test {operation} operation for {user.username}',
                    ip_address='127.0.0.1',
                    user_agent='Mozilla/5.0 (Test Browser)',
                    timestamp=timezone.now() - timedelta(hours=i),
                    success=True,
                    details={'test': True, 'user_id': user.id}
                )
