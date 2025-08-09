#!/usr/bin/env python3
"""
CipherChat Simple Server
A basic server for real-time communication between machines over network.
"""

import socket
import threading
import json
import sys
import os
from datetime import datetime

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

class CipherChatServer:
    """Simple relay server for CipherChat messages."""
    
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.clients = {}  # username -> socket
        self.messages = []  # message history
        
    def start_server(self):
        """Start the server."""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            print(f"🌐 CipherChat Server started on {self.host}:{self.port}")
            print("=" * 50)
            print("Waiting for connections...")
            
            while True:
                client_socket, address = self.server_socket.accept()
                print(f"🔗 New connection from {address}")
                
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except KeyboardInterrupt:
            print("\n🛑 Server shutting down...")
        except Exception as e:
            print(f"❌ Server error: {e}")
        finally:
            self.server_socket.close()
    
    def handle_client(self, client_socket, address):
        """Handle individual client connection."""
        username = None
        
        try:
            while True:
                # Receive data from client
                data = client_socket.recv(4096).decode('utf-8')
                if not data:
                    break
                
                try:
                    message = json.loads(data)
                    msg_type = message.get('type')
                    
                    if msg_type == 'register':
                        username = message.get('username')
                        self.clients[username] = client_socket
                        print(f"✅ User '{username}' registered from {address}")
                        
                        # Send confirmation
                        response = {'type': 'registered', 'username': username}
                        client_socket.send(json.dumps(response).encode('utf-8'))
                        
                    elif msg_type == 'message':
                        # Relay encrypted message to recipient
                        recipient = message.get('recipient')
                        sender = message.get('sender')
                        
                        if recipient in self.clients:
                            # Forward message to recipient
                            forward_msg = {
                                'type': 'incoming_message',
                                'from': sender,
                                'message_data': message.get('message_data'),
                                'timestamp': datetime.now().isoformat()
                            }
                            
                            self.clients[recipient].send(
                                json.dumps(forward_msg).encode('utf-8')
                            )
                            
                            print(f"📤 Message relayed: {sender} → {recipient}")
                            
                            # Confirm to sender
                            confirm = {'type': 'message_sent', 'to': recipient}
                            client_socket.send(json.dumps(confirm).encode('utf-8'))
                        else:
                            # Recipient not connected
                            error = {
                                'type': 'error',
                                'message': f"User '{recipient}' not connected"
                            }
                            client_socket.send(json.dumps(error).encode('utf-8'))
                    
                    elif msg_type == 'list_users':
                        # Send list of connected users
                        users_list = {
                            'type': 'users_list',
                            'users': list(self.clients.keys())
                        }
                        client_socket.send(json.dumps(users_list).encode('utf-8'))
                        
                except json.JSONDecodeError:
                    error = {'type': 'error', 'message': 'Invalid JSON'}
                    client_socket.send(json.dumps(error).encode('utf-8'))
                    
        except Exception as e:
            print(f"❌ Error handling client {address}: {e}")
        finally:
            # Clean up
            if username and username in self.clients:
                del self.clients[username]
                print(f"👋 User '{username}' disconnected")
            client_socket.close()

class CipherChatClient:
    """Simple client for connecting to CipherChat server."""
    
    def __init__(self, host='localhost', port=8888):
        self.host = host
        self.port = port
        self.socket = None
        self.username = None
        
    def connect(self, username):
        """Connect to server and register username."""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.username = username
            
            # Register username
            register_msg = {'type': 'register', 'username': username}
            self.socket.send(json.dumps(register_msg).encode('utf-8'))
            
            # Start listening for incoming messages
            listen_thread = threading.Thread(target=self.listen_for_messages)
            listen_thread.daemon = True
            listen_thread.start()
            
            print(f"✅ Connected to server as '{username}'")
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def listen_for_messages(self):
        """Listen for incoming messages from server."""
        try:
            while True:
                data = self.socket.recv(4096).decode('utf-8')
                if not data:
                    break
                
                try:
                    message = json.loads(data)
                    msg_type = message.get('type')
                    
                    if msg_type == 'incoming_message':
                        print(f"\n📥 New message from {message['from']}")
                        print(f"💾 Message data available for decryption")
                        # In real implementation, save to file for CipherChat to process
                        
                    elif msg_type == 'message_sent':
                        print(f"✅ Message delivered to {message['to']}")
                        
                    elif msg_type == 'error':
                        print(f"❌ Error: {message['message']}")
                        
                except json.JSONDecodeError:
                    print("❌ Received invalid message from server")
                    
        except Exception as e:
            print(f"❌ Error listening for messages: {e}")
    
    def send_message(self, recipient, message_data):
        """Send encrypted message through server."""
        try:
            msg = {
                'type': 'message',
                'sender': self.username,
                'recipient': recipient,
                'message_data': message_data
            }
            self.socket.send(json.dumps(msg).encode('utf-8'))
            
        except Exception as e:
            print(f"❌ Failed to send message: {e}")
    
    def disconnect(self):
        """Disconnect from server."""
        if self.socket:
            self.socket.close()
            print("👋 Disconnected from server")

def run_server():
    """Run the server."""
    server = CipherChatServer()
    server.start_server()

def run_client():
    """Run a test client."""
    username = input("Enter your username: ")
    client = CipherChatClient()
    
    if client.connect(username):
        print("\nCommands:")
        print("- 'quit' to exit")
        print("- 'send <username> <message>' to send message")
        
        try:
            while True:
                cmd = input(f"\n{username}> ").strip()
                
                if cmd == 'quit':
                    break
                elif cmd.startswith('send '):
                    parts = cmd.split(' ', 2)
                    if len(parts) >= 3:
                        recipient = parts[1]
                        message = parts[2]
                        client.send_message(recipient, message)
                    else:
                        print("Usage: send <username> <message>")
                
        except KeyboardInterrupt:
            pass
        finally:
            client.disconnect()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == 'client':
        run_client()
    else:
        print("🌐 CipherChat Simple Server")
        print("=" * 30)
        print("Usage:")
        print("  python simple_server.py        - Run server")
        print("  python simple_server.py client - Run test client")
        print("\nStarting server...")
        run_server()


