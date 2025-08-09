#!/usr/bin/env python3
"""
CipherChat Client - Connect to Remote Server
Easy connection script for connecting to CipherChat server from other machines.
"""

import socket
import threading
import json
import sys
import os
from datetime import datetime

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    COLORS_AVAILABLE = True
except ImportError:
    COLORS_AVAILABLE = False
    class Fore:
        RED = GREEN = YELLOW = BLUE = MAGENTA = CYAN = WHITE = RESET = ""
    class Style:
        BRIGHT = DIM = NORMAL = RESET_ALL = ""

class CipherChatNetworkClient:
    """Enhanced client for connecting to CipherChat server."""
    
    def __init__(self, server_ip, server_port=8888):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = None
        self.username = None
        self.connected = False
        
    def print_header(self):
        """Print client header."""
        print(f"\n{Fore.CYAN}{'='*60}")
        print(f"{Fore.CYAN}🌐 CipherChat Network Client")
        print(f"{Fore.CYAN}{'='*60}")
        print(f"{Fore.YELLOW}Connecting to: {self.server_ip}:{self.server_port}")
        print(f"{Fore.CYAN}{'='*60}\n")
        
    def connect(self, username):
        """Connect to server and register username."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.settimeout(10)  # 10 second timeout
            
            print(f"{Fore.YELLOW}🔄 Connecting to server...")
            self.socket.connect((self.server_ip, self.server_port))
            self.username = username
            
            # Register username
            register_msg = {'type': 'register', 'username': username}
            self.socket.send(json.dumps(register_msg).encode('utf-8'))
            
            # Wait for confirmation
            response = self.socket.recv(1024).decode('utf-8')
            response_data = json.loads(response)
            
            if response_data.get('type') == 'registered':
                self.connected = True
                print(f"{Fore.GREEN}✅ Connected successfully as '{username}'")
                
                # Start listening for incoming messages
                listen_thread = threading.Thread(target=self.listen_for_messages)
                listen_thread.daemon = True
                listen_thread.start()
                
                return True
            else:
                print(f"{Fore.RED}❌ Registration failed")
                return False
                
        except socket.timeout:
            print(f"{Fore.RED}❌ Connection timeout - server not responding")
            return False
        except ConnectionRefusedError:
            print(f"{Fore.RED}❌ Connection refused - server not running or firewall blocking")
            return False
        except Exception as e:
            print(f"{Fore.RED}❌ Connection failed: {e}")
            return False
    
    def listen_for_messages(self):
        """Listen for incoming messages from server."""
        try:
            while self.connected:
                data = self.socket.recv(4096).decode('utf-8')
                if not data:
                    break
                
                try:
                    message = json.loads(data)
                    msg_type = message.get('type')
                    
                    if msg_type == 'incoming_message':
                        print(f"\n{Fore.GREEN}📥 New message from {Fore.BRIGHT}{message['from']}")
                        print(f"{Fore.BLUE}⏰ Time: {message['timestamp']}")
                        
                        # Save message for CipherChat processing
                        filename = f"received_from_{message['from']}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                        os.makedirs("received_messages", exist_ok=True)
                        filepath = os.path.join("received_messages", filename)
                        
                        with open(filepath, 'w') as f:
                            json.dump(message['message_data'], f, indent=2)
                        
                        print(f"{Fore.CYAN}💾 Message saved to: {filepath}")
                        print(f"{Fore.YELLOW}🔓 Use CipherChat to decrypt: python cipherchat.py → Option 4")
                        print(f"{Fore.WHITE}{'─'*50}")
                        
                    elif msg_type == 'message_sent':
                        print(f"{Fore.GREEN}✅ Message delivered to {message['to']}")
                        
                    elif msg_type == 'error':
                        print(f"{Fore.RED}❌ Error: {message['message']}")
                        
                    elif msg_type == 'users_list':
                        print(f"\n{Fore.MAGENTA}👥 Connected users:")
                        for user in message['users']:
                            marker = f"{Fore.GREEN}*" if user == self.username else " "
                            print(f"{marker} {Fore.WHITE}{user}")
                        
                except json.JSONDecodeError:
                    print(f"{Fore.RED}❌ Received invalid message from server")
                    
        except Exception as e:
            if self.connected:
                print(f"\n{Fore.RED}❌ Error listening for messages: {e}")
    
    def send_encrypted_message(self, recipient, message_file):
        """Send encrypted message file through server."""
        try:
            # Load encrypted message from file
            with open(message_file, 'r') as f:
                message_data = json.load(f)
            
            # Send through server
            server_msg = {
                'type': 'message',
                'sender': self.username,
                'recipient': recipient,
                'message_data': message_data
            }
            
            self.socket.send(json.dumps(server_msg).encode('utf-8'))
            print(f"{Fore.YELLOW}📤 Sending encrypted message to {recipient}...")
            
        except FileNotFoundError:
            print(f"{Fore.RED}❌ Message file not found: {message_file}")
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to send message: {e}")
    
    def list_users(self):
        """Request list of connected users."""
        try:
            msg = {'type': 'list_users'}
            self.socket.send(json.dumps(msg).encode('utf-8'))
        except Exception as e:
            print(f"{Fore.RED}❌ Failed to request user list: {e}")
    
    def disconnect(self):
        """Disconnect from server."""
        self.connected = False
        if self.socket:
            self.socket.close()
            print(f"{Fore.YELLOW}👋 Disconnected from server")

def show_usage():
    """Show usage instructions."""
    print(f"""
{Fore.CYAN}📋 CipherChat Network Client Usage:
{Fore.CYAN}{'='*40}

{Fore.YELLOW}🔗 Connection:
{Fore.WHITE}python connect_to_server.py <server_ip>

{Fore.YELLOW}💬 Commands in client:
{Fore.WHITE}• list                     - Show connected users
{Fore.WHITE}• send <user> <file>       - Send encrypted message file
{Fore.WHITE}• help                     - Show this help
{Fore.WHITE}• quit                     - Disconnect and exit

{Fore.YELLOW}📝 Workflow:
{Fore.WHITE}1. Create encrypted message with CipherChat (Option 3)
{Fore.WHITE}2. Use 'send <username> <message_file.json>' here
{Fore.WHITE}3. Recipient gets notified and file saved
{Fore.WHITE}4. Recipient uses CipherChat (Option 4) to decrypt

{Fore.YELLOW}📁 File Locations:
{Fore.WHITE}• Outgoing: Use files from ./messages/
{Fore.WHITE}• Incoming: Saved to ./received_messages/

{Fore.YELLOW}🌐 Example:
{Fore.WHITE}python connect_to_server.py 192.168.1.100
{Fore.WHITE}Username: alice
{Fore.WHITE}alice> send bob alice_to_bob_20240115_143022.json
""")

def main():
    """Main client function."""
    if len(sys.argv) != 2:
        print(f"{Fore.RED}❌ Usage: python connect_to_server.py <server_ip>")
        show_usage()
        return
    
    server_ip = sys.argv[1]
    client = CipherChatNetworkClient(server_ip)
    
    client.print_header()
    
    username = input(f"{Fore.CYAN}Enter your username: {Style.RESET_ALL}")
    if not username:
        print(f"{Fore.RED}❌ Username cannot be empty")
        return
    
    if client.connect(username):
        print(f"\n{Fore.GREEN}🎉 Connected! Available commands:")
        print(f"{Fore.WHITE}• list              - Show connected users")
        print(f"{Fore.WHITE}• send <user> <file> - Send encrypted message")
        print(f"{Fore.WHITE}• help              - Show detailed help")
        print(f"{Fore.WHITE}• quit              - Exit")
        print(f"{Fore.CYAN}{'─'*50}")
        
        try:
            while client.connected:
                try:
                    cmd = input(f"\n{Fore.MAGENTA}{username}> {Style.RESET_ALL}").strip()
                    
                    if not cmd:
                        continue
                        
                    if cmd == 'quit':
                        break
                    elif cmd == 'list':
                        client.list_users()
                    elif cmd == 'help':
                        show_usage()
                    elif cmd.startswith('send '):
                        parts = cmd.split(' ', 2)
                        if len(parts) >= 3:
                            recipient = parts[1]
                            message_file = parts[2]
                            client.send_encrypted_message(recipient, message_file)
                        else:
                            print(f"{Fore.RED}Usage: send <username> <message_file>")
                    else:
                        print(f"{Fore.RED}Unknown command. Type 'help' for usage.")
                        
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}Interrupted by user")
                    break
                except EOFError:
                    break
                    
        except Exception as e:
            print(f"{Fore.RED}❌ Client error: {e}")
        finally:
            client.disconnect()
    else:
        print(f"\n{Fore.RED}❌ Failed to connect to server")
        print(f"{Fore.YELLOW}💡 Make sure:")
        print(f"{Fore.WHITE}• Server is running on {server_ip}:8888")
        print(f"{Fore.WHITE}• Network allows connections")
        print(f"{Fore.WHITE}• Firewall permits port 8888")

if __name__ == "__main__":
    main()
