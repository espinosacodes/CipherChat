#!/usr/bin/env python3
"""
Setup script for CipherChat
Provides easy installation and setup of the secure communication system.
"""

import os
import sys
import subprocess
from pathlib import Path

def print_header():
    """Print setup header."""
    print("🔐 CipherChat Setup")
    print("=" * 50)
    print("Setting up secure communication system...")
    print("=" * 50)

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 7):
        print("❌ Error: Python 3.7 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def install_dependencies():
    """Install required dependencies."""
    print("\n📦 Installing dependencies...")
    
    try:
        # Check if pip is available
        subprocess.run([sys.executable, "-m", "pip", "--version"], 
                      check=True, capture_output=True)
        
        # Install requirements
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✅ Dependencies installed successfully")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False
    except FileNotFoundError:
        print("❌ pip not found. Please install pip first.")
        return False

def create_directories():
    """Create necessary directories."""
    print("\n📁 Creating directories...")
    
    directories = ["keys", "messages"]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"✅ Created directory: {directory}/")

def test_installation():
    """Test if the installation works."""
    print("\n🧪 Testing installation...")
    
    try:
        # Test imports
        sys.path.insert(0, "src")
        from src.crypto_engine import CryptoEngine
        from src.key_manager import KeyManager
        from src.secure_channel import SecureChannel
        
        # Test basic functionality
        crypto = CryptoEngine()
        key_manager = KeyManager("test_keys")
        
        # Clean up test directory
        import shutil
        if Path("test_keys").exists():
            shutil.rmtree("test_keys")
            
        print("✅ Installation test passed")
        return True
        
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

def show_usage_instructions():
    """Show usage instructions."""
    print("\n🚀 Setup Complete!")
    print("=" * 50)
    print("You can now use CipherChat in the following ways:")
    print()
    print("1. Interactive Mode:")
    print("   python cipherchat.py")
    print()
    print("2. Demo Mode:")
    print("   python demo.py")
    print()
    print("3. Performance Test:")
    print("   python demo.py --performance")
    print()
    print("4. Programmatic Usage:")
    print("   from src.key_manager import KeyManager")
    print("   from src.secure_channel import SecureChannel")
    print()
    print("📖 For detailed documentation, see README.md")
    print("🔐 Stay secure with CipherChat!")

def main():
    """Main setup function."""
    print_header()
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("\n❌ Setup failed during dependency installation")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Test installation
    if not test_installation():
        print("\n❌ Setup failed during testing")
        sys.exit(1)
    
    # Show usage instructions
    show_usage_instructions()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Setup interrupted by user")
    except Exception as e:
        print(f"\n❌ Setup failed with error: {e}")
        sys.exit(1)

