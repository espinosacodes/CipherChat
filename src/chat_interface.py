"""
CipherChat Interactive CLI Interface
Provides a user-friendly command-line interface for secure messaging.
"""

import os
import sys
import json
from typing import Optional, List
from pathlib import Path

try:
    from colorama import init, Fore, Back, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    # Fallback color class
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    
    class Back:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ""

from .key_manager import KeyManager
from .secure_channel import SecureChannel, SecureMessage


class ChatInterface:
    """
    Interactive command-line interface for CipherChat.
    """
    
    def __init__(self):
        """Initialize the chat interface."""
        self.key_manager = KeyManager()
        self.secure_channel = SecureChannel(self.key_manager)
        self.current_user = None
        self.messages_dir = Path("messages")
        self.messages_dir.mkdir(exist_ok=True)
        
    def print_header(self):
        """Print the application header."""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}🔐 CipherChat - Secure Communication System")
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}End-to-End Encrypted Messaging with RSA + AES")
        print(f"{Fore.GREEN}✅ Public-Key Cryptography  ✅ Digital Signatures")
        print(f"{Fore.GREEN}✅ Tamper-Proof Messages   ✅ Secure Key Exchange")
        print(f"{Fore.CYAN}{'='*60}\n")
        
    def print_menu(self):
        """Print the main menu."""
        print(f"\n{Fore.MAGENTA}📋 Main Menu:")
        print(f"{Fore.WHITE}1. 👤 User Management")
        print(f"{Fore.WHITE}2. 🔑 Key Management") 
        print(f"{Fore.WHITE}3. 💬 Send Message")
        print(f"{Fore.WHITE}4. 📥 Receive Message")
        print(f"{Fore.WHITE}5. 🔄 Key Exchange")
        print(f"{Fore.WHITE}6. 📊 View Messages")
        print(f"{Fore.WHITE}7. ❓ Help")
        print(f"{Fore.WHITE}8. 🚪 Exit")
        
    def print_user_menu(self):
        """Print the user management menu."""
        print(f"\n{Fore.MAGENTA}👤 User Management:")
        print(f"{Fore.WHITE}1. Create New User")
        print(f"{Fore.WHITE}2. Select User")
        print(f"{Fore.WHITE}3. List Users")
        print(f"{Fore.WHITE}4. Delete User")
        print(f"{Fore.WHITE}5. Back to Main Menu")
        
    def print_key_menu(self):
        """Print the key management menu."""
        print(f"\n{Fore.MAGENTA}🔑 Key Management:")
        print(f"{Fore.WHITE}1. Export My Public Key")
        print(f"{Fore.WHITE}2. Import Someone's Public Key")
        print(f"{Fore.WHITE}3. List Imported Keys")
        print(f"{Fore.WHITE}4. Back to Main Menu")
        
    def get_input(self, prompt: str) -> str:
        """Get user input with colored prompt."""
        return input(f"{Fore.CYAN}❯ {prompt}: {Style.RESET_ALL}")
        
    def print_success(self, message: str):
        """Print success message."""
        print(f"{Fore.GREEN}✅ {message}")
        
    def print_error(self, message: str):
        """Print error message."""
        print(f"{Fore.RED}❌ {message}")
        
    def print_info(self, message: str):
        """Print info message."""
        print(f"{Fore.BLUE}ℹ️  {message}")
        
    def create_user(self):
        """Create a new user and generate keys."""
        username = self.get_input("Enter username")
        
        if not username:
            self.print_error("Username cannot be empty")
            return
            
        if self.key_manager.user_exists(username):
            self.print_error(f"User '{username}' already exists")
            return
            
        try:
            private_key_path, public_key_path = self.key_manager.generate_user_keys(username)
            self.print_success(f"User '{username}' created successfully")
            self.print_info(f"Keys stored in: {Path(private_key_path).parent}")
        except Exception as e:
            self.print_error(f"Failed to create user: {e}")
            
    def select_user(self):
        """Select the current user."""
        users = self.key_manager.list_users()
        
        if not users:
            self.print_error("No users found. Create a user first.")
            return
            
        print(f"\n{Fore.YELLOW}Available users:")
        for i, user in enumerate(users, 1):
            print(f"{Fore.WHITE}{i}. {user}")
            
        try:
            choice = int(self.get_input("Select user number"))
            if 1 <= choice <= len(users):
                self.current_user = users[choice - 1]
                self.print_success(f"Selected user: {self.current_user}")
            else:
                self.print_error("Invalid choice")
        except ValueError:
            self.print_error("Please enter a valid number")
            
    def list_users(self):
        """List all users."""
        users = self.key_manager.list_users()
        
        if not users:
            self.print_info("No users found")
            return
            
        print(f"\n{Fore.YELLOW}Users with generated keys:")
        for user in users:
            marker = f"{Fore.GREEN}*" if user == self.current_user else " "
            print(f"{marker} {Fore.WHITE}{user}")
            
    def delete_user(self):
        """Delete a user and their keys."""
        users = self.key_manager.list_users()
        
        if not users:
            self.print_error("No users found")
            return
            
        self.list_users()
        username = self.get_input("Enter username to delete")
        
        if username not in users:
            self.print_error(f"User '{username}' not found")
            return
            
        confirm = self.get_input(f"Are you sure you want to delete '{username}'? (yes/no)")
        if confirm.lower() == 'yes':
            if self.key_manager.delete_user_keys(username):
                if self.current_user == username:
                    self.current_user = None
                    self.print_info("Current user cleared")
            
    def export_public_key(self):
        """Export current user's public key."""
        if not self.current_user:
            self.print_error("No user selected. Select a user first.")
            return
            
        export_path = self.get_input(f"Export path (or press Enter for default)")
        if not export_path:
            export_path = None
            
        self.key_manager.export_public_key(self.current_user, export_path)
        
    def import_public_key(self):
        """Import someone's public key."""
        username = self.get_input("Enter the username to associate with this key")
        key_file = self.get_input("Enter path to the public key file")
        
        if not os.path.exists(key_file):
            self.print_error(f"File not found: {key_file}")
            return
            
        self.key_manager.import_public_key(username, key_file)
        
    def list_imported_keys(self):
        """List imported public keys."""
        imported_dir = self.key_manager.keys_dir / "imported"
        if not imported_dir.exists():
            self.print_info("No imported keys found")
            return
            
        keys = []
        for key_file in imported_dir.glob("*_public.pem"):
            username = key_file.stem.replace("_public", "")
            keys.append(username)
            
        if not keys:
            self.print_info("No imported keys found")
        else:
            print(f"\n{Fore.YELLOW}Imported public keys:")
            for key in sorted(keys):
                print(f"  {Fore.WHITE}{key}")
                
    def send_message(self):
        """Send an encrypted message."""
        if not self.current_user:
            self.print_error("No user selected. Select a user first.")
            return
            
        recipient = self.get_input("Enter recipient username")
        message = self.get_input("Enter your message")
        
        if not recipient or not message:
            self.print_error("Recipient and message cannot be empty")
            return
            
        secure_message = self.secure_channel.send_message(
            self.current_user, recipient, message
        )
        
        if secure_message:
            # Save message to file
            timestamp_str = secure_message.get_timestamp_str().replace(":", "-").replace(" ", "_")
            filename = f"{self.current_user}_to_{recipient}_{timestamp_str}.json"
            filepath = self.messages_dir / filename
            
            with open(filepath, 'w') as f:
                f.write(self.secure_channel.export_message_for_transmission(secure_message))
                
            self.print_success(f"Message encrypted and saved to: {filepath}")
            self.print_info("Share this file with the recipient to deliver the message")
            
    def receive_message(self):
        """Receive and decrypt a message."""
        if not self.current_user:
            self.print_error("No user selected. Select a user first.")
            return
            
        message_file = self.get_input("Enter path to the encrypted message file")
        
        if not os.path.exists(message_file):
            self.print_error(f"File not found: {message_file}")
            return
            
        try:
            with open(message_file, 'r') as f:
                message_data = json.load(f)
                
            if message_data.get('message_type') != 'secure_message':
                self.print_error("Invalid message file format")
                return
                
            decrypted_message = self.secure_channel.receive_message(
                message_data, self.current_user
            )
            
            if decrypted_message:
                sender = message_data['sender']
                timestamp = message_data['timestamp']
                secure_msg = SecureMessage.from_dict(message_data)
                
                print(f"\n{Fore.GREEN}📨 Message Received:")
                print(f"{Fore.YELLOW}From: {Fore.WHITE}{sender}")
                print(f"{Fore.YELLOW}Time: {Fore.WHITE}{secure_msg.get_timestamp_str()}")
                print(f"{Fore.YELLOW}Message: {Fore.WHITE}{decrypted_message}")
                
        except Exception as e:
            self.print_error(f"Failed to process message: {e}")
            
    def key_exchange(self):
        """Perform key exchange with another user."""
        if not self.current_user:
            self.print_error("No user selected. Select a user first.")
            return
            
        print(f"\n{Fore.MAGENTA}🔄 Key Exchange Options:")
        print(f"{Fore.WHITE}1. Send my public key to someone")
        print(f"{Fore.WHITE}2. Process received key exchange")
        
        choice = self.get_input("Choose option (1-2)")
        
        if choice == "1":
            recipient = self.get_input("Enter recipient username")
            key_exchange_msg = self.secure_channel.create_key_exchange_message(
                self.current_user, recipient
            )
            
            if key_exchange_msg:
                filename = f"key_exchange_{self.current_user}_to_{recipient}.json"
                filepath = self.messages_dir / filename
                
                with open(filepath, 'w') as f:
                    json.dump(key_exchange_msg, f, indent=2)
                    
                self.print_success(f"Key exchange message saved to: {filepath}")
                self.print_info("Share this file with the recipient")
                
        elif choice == "2":
            key_file = self.get_input("Enter path to key exchange file")
            
            if not os.path.exists(key_file):
                self.print_error(f"File not found: {key_file}")
                return
                
            try:
                with open(key_file, 'r') as f:
                    key_data = json.load(f)
                    
                if key_data.get('message_type') != 'key_exchange':
                    self.print_error("Invalid key exchange file format")
                    return
                    
                success = self.secure_channel.process_key_exchange(key_data)
                if success:
                    self.print_success("Key exchange processed successfully")
                    
            except Exception as e:
                self.print_error(f"Failed to process key exchange: {e}")
        else:
            self.print_error("Invalid choice")
            
    def view_messages(self):
        """View saved messages."""
        if not self.messages_dir.exists():
            self.print_info("No messages found")
            return
            
        message_files = list(self.messages_dir.glob("*.json"))
        
        if not message_files:
            self.print_info("No messages found")
            return
            
        print(f"\n{Fore.YELLOW}📁 Saved Messages:")
        for i, msg_file in enumerate(sorted(message_files), 1):
            print(f"{Fore.WHITE}{i}. {msg_file.name}")
            
    def show_help(self):
        """Show help information."""
        print(f"\n{Fore.CYAN}🆘 CipherChat Help")
        print(f"{Fore.CYAN}{'='*50}")
        print(f"{Fore.YELLOW}Getting Started:")
        print(f"{Fore.WHITE}1. Create a user account (generates your key pair)")
        print(f"{Fore.WHITE}2. Select your user to become active")
        print(f"{Fore.WHITE}3. Exchange public keys with other users")
        print(f"{Fore.WHITE}4. Send and receive encrypted messages")
        
        print(f"\n{Fore.YELLOW}Security Features:")
        print(f"{Fore.WHITE}• RSA + AES hybrid encryption")
        print(f"{Fore.WHITE}• Digital signatures for authentication")
        print(f"{Fore.WHITE}• Tamper-proof message verification")
        print(f"{Fore.WHITE}• Secure key exchange protocol")
        
        print(f"\n{Fore.YELLOW}File Locations:")
        print(f"{Fore.WHITE}• Keys: ./keys/[username]/")
        print(f"{Fore.WHITE}• Messages: ./messages/")
        print(f"{Fore.WHITE}• Imported keys: ./keys/imported/")
        
    def run(self):
        """Run the main application loop."""
        self.print_header()
        
        while True:
            # Show current user status
            if self.current_user:
                print(f"\n{Fore.GREEN}Current user: {Style.BRIGHT}{self.current_user}")
            else:
                print(f"\n{Fore.YELLOW}No user selected")
                
            self.print_menu()
            
            choice = self.get_input("Choose an option (1-8)")
            
            if choice == "1":
                while True:
                    self.print_user_menu()
                    user_choice = self.get_input("Choose an option (1-5)")
                    
                    if user_choice == "1":
                        self.create_user()
                    elif user_choice == "2":
                        self.select_user()
                    elif user_choice == "3":
                        self.list_users()
                    elif user_choice == "4":
                        self.delete_user()
                    elif user_choice == "5":
                        break
                    else:
                        self.print_error("Invalid choice")
                        
            elif choice == "2":
                while True:
                    self.print_key_menu()
                    key_choice = self.get_input("Choose an option (1-4)")
                    
                    if key_choice == "1":
                        self.export_public_key()
                    elif key_choice == "2":
                        self.import_public_key()
                    elif key_choice == "3":
                        self.list_imported_keys()
                    elif key_choice == "4":
                        break
                    else:
                        self.print_error("Invalid choice")
                        
            elif choice == "3":
                self.send_message()
            elif choice == "4":
                self.receive_message()
            elif choice == "5":
                self.key_exchange()
            elif choice == "6":
                self.view_messages()
            elif choice == "7":
                self.show_help()
            elif choice == "8":
                print(f"\n{Fore.CYAN}👋 Thanks for using CipherChat!")
                print(f"{Fore.GREEN}Stay secure! 🔐")
                break
            else:
                self.print_error("Invalid choice. Please try again.")
                
            # Pause before showing menu again
            input(f"\n{Fore.CYAN}Press Enter to continue...")


def main():
    """Main entry point for the application."""
    try:
        chat = ChatInterface()
        chat.run()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.YELLOW}Application interrupted by user")
        print(f"{Fore.GREEN}Goodbye! 👋")
    except Exception as e:
        print(f"\n{Fore.RED}Unexpected error: {e}")
        print(f"{Fore.YELLOW}Please report this issue")


if __name__ == "__main__":
    main()

