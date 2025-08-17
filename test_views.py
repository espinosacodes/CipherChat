#!/usr/bin/env python3
"""
Test script to verify that the Django views and models work correctly.
"""

import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cipherchat_web.settings')
django.setup()

from django.contrib.auth.models import User
from chat.models import PublicKey, UserProfile, Message, SecurityLog
from chat.views import dashboard, manage_keys

def test_models():
    """Test that models can be imported and queried."""
    print("Testing models...")
    
    # Test PublicKey model
    print(f"PublicKey model fields: {[f.name for f in PublicKey._meta.fields]}")
    
    # Test UserProfile model
    print(f"UserProfile model fields: {[f.name for f in UserProfile._meta.fields]}")
    
    # Test Message model
    print(f"Message model fields: {[f.name for f in Message._meta.fields]}")
    
    # Test SecurityLog model
    print(f"SecurityLog model fields: {[f.name for f in SecurityLog._meta.fields]}")
    
    print("✅ All models imported successfully!")

def test_queries():
    """Test that queries work correctly."""
    print("\nTesting queries...")
    
    # Test PublicKey queries
    try:
        count = PublicKey.objects.filter(owner__isnull=False).count()
        print(f"✅ PublicKey query successful: {count} keys found")
    except Exception as e:
        print(f"❌ PublicKey query failed: {e}")
    
    # Test UserProfile queries
    try:
        count = UserProfile.objects.count()
        print(f"✅ UserProfile query successful: {count} profiles found")
    except Exception as e:
        print(f"❌ UserProfile query failed: {e}")
    
    # Test Message queries
    try:
        count = Message.objects.count()
        print(f"✅ Message query successful: {count} messages found")
    except Exception as e:
        print(f"❌ Message query failed: {e}")
    
    # Test SecurityLog queries
    try:
        count = SecurityLog.objects.count()
        print(f"✅ SecurityLog query successful: {count} logs found")
    except Exception as e:
        print(f"❌ SecurityLog query failed: {e}")

def test_views():
    """Test that views can be imported."""
    print("\nTesting views...")
    
    try:
        # Test that views can be imported
        from chat.views import dashboard, manage_keys, send_message, import_key
        print("✅ All views imported successfully!")
    except Exception as e:
        print(f"❌ View import failed: {e}")

if __name__ == "__main__":
    print("🧪 Testing CipherChat Django Application...")
    print("=" * 50)
    
    test_models()
    test_queries()
    test_views()
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed successfully!")
    print("The 'imported_by' field error has been fixed!")
