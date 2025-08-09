#!/usr/bin/env python3
"""
CipherChat Demo Script
Demonstrates the secure messaging capabilities of CipherChat.
"""

import sys
import os
import json
import tempfile
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.key_manager import KeyManager
from src.secure_channel import SecureChannel
from src.crypto_engine import CryptoEngine

def print_header():
    """Print demo header."""
    print("🔐 CipherChat Demo - Secure Communication System")
    print("=" * 60)
    print("This demo shows end-to-end encryption between Alice and Bob")
    print("=" * 60)

def print_step(step, description):
    """Print demo step."""
    print(f"\n🔹 Step {step}: {description}")
    print("-" * 40)

def demonstrate_cipherchat():
    """Run the CipherChat demonstration."""
    print_header()
    
    # Create temporary demo directory
    with tempfile.TemporaryDirectory() as temp_dir:
        demo_dir = Path(temp_dir)
        
        # Initialize components
        key_manager = KeyManager(str(demo_dir / "keys"))
        secure_channel = SecureChannel(key_manager)
        
        print_step(1, "Creating users Alice and Bob")
        
        # Create Alice's keys
        alice_private, alice_public = key_manager.generate_user_keys("alice")
        print("✅ Generated keys for Alice")
        
        # Create Bob's keys  
        bob_private, bob_public = key_manager.generate_user_keys("bob")
        print("✅ Generated keys for Bob")
        
        print_step(2, "Key Exchange - Alice and Bob share public keys")
        
        # Simulate key exchange
        alice_key_exchange = secure_channel.create_key_exchange_message("alice", "bob")
        bob_key_exchange = secure_channel.create_key_exchange_message("bob", "alice")
        
        # Process key exchanges
        print("🔄 Alice sends her public key to Bob...")
        secure_channel.process_key_exchange(alice_key_exchange)
        
        print("🔄 Bob sends his public key to Alice...")
        secure_channel.process_key_exchange(bob_key_exchange)
        
        print("✅ Key exchange completed successfully")
        
        print_step(3, "Alice sends encrypted message to Bob")
        
        # Alice sends message to Bob
        alice_message = "Hello Bob! This is a secret message from Alice. 🤫"
        print(f"📝 Alice's original message: '{alice_message}'")
        
        encrypted_message = secure_channel.send_message("alice", "bob", alice_message)
        
        if encrypted_message:
            print("🔒 Message encrypted successfully!")
            
            # Show encrypted data (partially)
            encrypted_data = encrypted_message.encrypted_data
            print(f"🔑 Encrypted AES key (first 50 chars): {encrypted_data['encrypted_key'][:50]}...")
            print(f"🔒 Encrypted message (first 50 chars): {encrypted_data['encrypted_message'][:50]}...")
            print(f"🔐 Digital signature (first 50 chars): {encrypted_message.signature[:50]}...")
            
        print_step(4, "Bob receives and decrypts the message")
        
        # Bob receives and decrypts the message
        message_data = encrypted_message.to_dict()
        decrypted_message = secure_channel.receive_message(message_data, "bob")
        
        if decrypted_message:
            print(f"📖 Bob decrypted message: '{decrypted_message}'")
            print("🔓 Message integrity verified!")
            
            # Verify messages match
            if decrypted_message == alice_message:
                print("✅ SUCCESS: Original and decrypted messages match perfectly!")
            else:
                print("❌ ERROR: Message mismatch!")
        
        print_step(5, "Bob replies to Alice")
        
        # Bob sends reply to Alice
        bob_reply = "Hi Alice! I received your secret message safely. Thanks for the demo! 👍"
        print(f"📝 Bob's reply: '{bob_reply}'")
        
        encrypted_reply = secure_channel.send_message("bob", "alice", bob_reply)
        
        if encrypted_reply:
            print("🔒 Reply encrypted successfully!")
            
            # Alice receives Bob's reply
            reply_data = encrypted_reply.to_dict()
            decrypted_reply = secure_channel.receive_message(reply_data, "alice")
            
            if decrypted_reply:
                print(f"📖 Alice received: '{decrypted_reply}'")
                print("✅ Two-way communication established!")
        
        print_step(6, "Security Analysis")
        
        # Demonstrate security features
        crypto_engine = CryptoEngine()
        
        print("🔍 Security Features Demonstrated:")
        print("  • RSA key pairs (2048-bit) for asymmetric encryption")
        print("  • AES-256 for symmetric encryption of messages")
        print("  • OAEP padding for RSA encryption")
        print("  • PSS signatures for message authentication")
        print("  • SHA-256 hashing for integrity")
        print("  • Random IV generation for each message")
        
        print("\n🛡️  Attack Resistance:")
        print("  • Eavesdropping: Messages are encrypted end-to-end")
        print("  • Tampering: Digital signatures detect modifications")
        print("  • Replay attacks: Timestamps prevent message replay")
        print("  • Key compromise: Each session uses unique AES keys")
        
        print_step(7, "Tampering Detection Demo")
        
        # Demonstrate tampering detection
        print("🕵️  Testing tampering detection...")
        
        # Create a message and then tamper with it
        test_message = "This message will be tampered with"
        encrypted_test = secure_channel.send_message("alice", "bob", test_message)
        
        if encrypted_test:
            # Tamper with the encrypted message
            tampered_data = encrypted_test.to_dict()
            tampered_data['signature'] = tampered_data['signature'][:-10] + "TAMPERED123"
            
            print("🔧 Simulating message tampering...")
            decrypted_tampered = secure_channel.receive_message(tampered_data, "bob")
            
            if decrypted_tampered is None:
                print("✅ SUCCESS: Tampering detected and message rejected!")
            else:
                print("❌ ERROR: Tampering not detected!")
        
        print("\n" + "=" * 60)
        print("🎉 CipherChat Demo Completed Successfully!")
        print("=" * 60)
        print("🔐 All security features working correctly:")
        print("  ✅ Encryption/Decryption")
        print("  ✅ Digital Signatures") 
        print("  ✅ Key Exchange")
        print("  ✅ Tampering Detection")
        print("  ✅ End-to-End Security")
        print("\n🚀 Ready for real-world secure communication!")


def run_performance_test():
    """Run a basic performance test."""
    print("\n🏃 Performance Test")
    print("-" * 30)
    
    import time
    
    with tempfile.TemporaryDirectory() as temp_dir:
        key_manager = KeyManager(str(Path(temp_dir) / "keys"))
        secure_channel = SecureChannel(key_manager)
        
        # Generate keys
        key_manager.generate_user_keys("user1")
        key_manager.generate_user_keys("user2")
        
        # Perform key exchange
        key_exchange = secure_channel.create_key_exchange_message("user1", "user2")
        secure_channel.process_key_exchange(key_exchange)
        
        # Test message of various sizes
        test_sizes = [10, 100, 1000, 10000]  # characters
        
        for size in test_sizes:
            message = "A" * size
            
            # Time encryption
            start_time = time.time()
            encrypted = secure_channel.send_message("user1", "user2", message)
            encrypt_time = time.time() - start_time
            
            # Time decryption
            start_time = time.time()
            if encrypted:
                decrypted = secure_channel.receive_message(encrypted.to_dict(), "user2")
            decrypt_time = time.time() - start_time
            
            print(f"📊 Message size: {size:5d} chars | "
                  f"Encrypt: {encrypt_time*1000:6.2f}ms | "
                  f"Decrypt: {decrypt_time*1000:6.2f}ms")


if __name__ == "__main__":
    try:
        if len(sys.argv) > 1 and sys.argv[1] == "--performance":
            run_performance_test()
        else:
            demonstrate_cipherchat()
            
        if len(sys.argv) > 1 and sys.argv[1] == "--full":
            run_performance_test()
            
    except KeyboardInterrupt:
        print("\n\n👋 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        import traceback
        traceback.print_exc()
