#!/usr/bin/env python3
"""
CipherChat Quick Client Setup
Rapid installation script for client machines to connect to CipherChat server.
"""

import os
import sys
import subprocess
import urllib.request
import json
from pathlib import Path

def print_header():
    """Print setup header."""
    print("🚀 CipherChat Quick Client Setup")
    print("=" * 40)
    print("Setting up client for remote CipherChat server...")
    print()

def check_requirements():
    """Check if basic requirements are met."""
    print("🔍 Checking requirements...")
    
    # Check Python version
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required")
        return False
    print(f"✅ Python {sys.version.split()[0]}")
    
    # Check pip
    try:
        import pip
        print("✅ pip available")
    except ImportError:
        print("❌ pip not found")
        return False
    
    return True

def create_minimal_client():
    """Create minimal client installation."""
    print("\n📦 Creating minimal client...")
    
    # Create directory structure
    client_dir = Path("cipherchat_client")
    client_dir.mkdir(exist_ok=True)
    
    src_dir = client_dir / "src"
    src_dir.mkdir(exist_ok=True)
    
    # Create minimal requirements
    requirements = """cryptography>=41.0.0
colorama>=0.4.6"""
    
    with open(client_dir / "requirements.txt", 'w') as f:
        f.write(requirements)
    
    # Copy essential files
    essential_files = [
        "connect_to_server.py",
        "src/crypto_engine.py",
        "src/key_manager.py", 
        "src/secure_channel.py",
        "src/__init__.py"
    ]
    
    print("📄 Copying essential files...")
    for file_path in essential_files:
        src_file = Path(file_path)
        if src_file.exists():
            dest_file = client_dir / file_path
            dest_file.parent.mkdir(exist_ok=True)
            
            # Copy file content
            with open(src_file, 'r') as f:
                content = f.read()
            with open(dest_file, 'w') as f:
                f.write(content)
            print(f"✅ Copied {file_path}")
        else:
            print(f"⚠️  File not found: {file_path}")
    
    return client_dir

def create_client_launcher(client_dir, server_ip):
    """Create launcher script for easy connection."""
    launcher_content = f"""#!/usr/bin/env python3
# CipherChat Client Launcher
import os
import sys

# Change to client directory
os.chdir(r"{client_dir.absolute()}")

# Add src to path
sys.path.insert(0, "src")

# Run client
os.system("python connect_to_server.py {server_ip}")
"""
    
    launcher_file = client_dir / "start_client.py"
    with open(launcher_file, 'w') as f:
        f.write(launcher_content)
    
    # Create batch file for Windows
    batch_content = f"""@echo off
cd /d "{client_dir.absolute()}"
python start_client.py
pause
"""
    
    batch_file = client_dir / "start_client.bat"
    with open(batch_file, 'w') as f:
        f.write(batch_content)
    
    print(f"✅ Created launcher: {launcher_file}")
    print(f"✅ Created batch file: {batch_file}")

def install_dependencies(client_dir):
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    
    requirements_file = client_dir / "requirements.txt"
    
    try:
        # Create virtual environment
        venv_dir = client_dir / "venv"
        subprocess.run([
            sys.executable, "-m", "venv", str(venv_dir)
        ], check=True)
        
        # Determine pip path
        if os.name == 'nt':  # Windows
            pip_path = venv_dir / "Scripts" / "pip"
        else:  # Linux/Mac
            pip_path = venv_dir / "bin" / "pip"
        
        # Install requirements
        subprocess.run([
            str(pip_path), "install", "-r", str(requirements_file)
        ], check=True)
        
        print("✅ Dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def create_usage_instructions(client_dir, server_ip):
    """Create usage instructions file."""
    instructions = f"""🔐 CipherChat Client - Usage Instructions
{'='*50}

📂 Installation Location: {client_dir.absolute()}

🚀 Quick Start:
1. Double-click: start_client.bat (Windows) or run start_client.py
2. Enter your username when prompted
3. Use commands to communicate

💬 Available Commands:
• list                     - Show connected users
• send <user> <file>       - Send encrypted message file
• help                     - Show detailed help
• quit                     - Disconnect and exit

📝 Sending Messages:
1. Create encrypted message with full CipherChat:
   - Install full CipherChat on your machine
   - Use Option 3 (Send Message) to create encrypted file
   - Note the filename (e.g., alice_to_bob_20240115_143022.json)

2. Send via network client:
   - Run this client: start_client.py
   - Use: send <recipient> <message_file.json>

📥 Receiving Messages:
1. Messages automatically saved to: received_messages/
2. Copy file to full CipherChat installation
3. Use Option 4 (Receive Message) to decrypt

🌐 Server Information:
• Server IP: {server_ip}
• Server Port: 8888

🔧 Troubleshooting:
• Make sure server is running
• Check firewall settings
• Verify network connectivity
• Ensure port 8888 is open

📞 Full CipherChat Installation:
For complete functionality, install full CipherChat:
git clone <repository>
cd CipherChat
python setup.py

---
🔐 Secure messaging with CipherChat!
"""
    
    with open(client_dir / "README.txt", 'w') as f:
        f.write(instructions)
    
    print(f"✅ Created instructions: {client_dir / 'README.txt'}")

def main():
    """Main setup function."""
    print_header()
    
    if not check_requirements():
        print("\n❌ Requirements not met. Please install Python 3.7+ and pip.")
        return
    
    # Get server IP
    server_ip = input("\n🌐 Enter CipherChat server IP address: ").strip()
    if not server_ip:
        print("❌ Server IP required")
        return
    
    try:
        # Create client installation
        client_dir = create_minimal_client()
        
        # Install dependencies
        if install_dependencies(client_dir):
            # Create launcher
            create_client_launcher(client_dir, server_ip)
            
            # Create instructions
            create_usage_instructions(client_dir, server_ip)
            
            print(f"\n🎉 Client setup complete!")
            print(f"📂 Installation: {client_dir.absolute()}")
            print(f"🚀 To start: run start_client.py or start_client.bat")
            print(f"📖 Instructions: README.txt")
            
        else:
            print(f"\n❌ Setup failed during dependency installation")
            
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")

if __name__ == "__main__":
    main()
