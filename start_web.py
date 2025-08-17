#!/usr/bin/env python3
"""
CipherChat Web Application Startup Script
This script helps you start the Django web application.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible."""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_dependencies():
    """Check if required packages are installed."""
    try:
        import django
        print(f"✅ Django {django.get_version()}")
        return True
    except ImportError:
        print("❌ Django is not installed. Installing dependencies...")
        return False

def install_dependencies():
    """Install required dependencies."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies.")
        return False

def check_database():
    """Check if database migrations are needed."""
    if not Path("db.sqlite3").exists():
        print("📊 Database not found. Running migrations...")
        try:
            subprocess.check_call([sys.executable, "manage.py", "makemigrations"])
            subprocess.check_call([sys.executable, "manage.py", "migrate"])
            print("✅ Database initialized successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to initialize database.")
            return False
    else:
        print("✅ Database exists.")
    return True

def create_superuser():
    """Ask if user wants to create a superuser."""
    response = input("\n🤔 Would you like to create a superuser account? (y/n): ").lower().strip()
    if response in ['y', 'yes']:
        try:
            subprocess.check_call([sys.executable, "manage.py", "createsuperuser"])
            print("✅ Superuser created successfully!")
        except subprocess.CalledProcessError:
            print("❌ Failed to create superuser.")

def start_server():
    """Start the Django development server."""
    print("\n🚀 Starting CipherChat web application...")
    print("📍 The application will be available at: http://127.0.0.1:8000/")
    print("🛑 Press Ctrl+C to stop the server")
    print("\n" + "="*60)
    
    try:
        subprocess.check_call([sys.executable, "manage.py", "runserver"])
    except subprocess.CalledProcessError:
        print("❌ Failed to start the server.")
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped. Goodbye!")

def main():
    """Main startup function."""
    print("🔐 CipherChat Web Application")
    print("="*40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check and install dependencies
    if not check_dependencies():
        if not install_dependencies():
            return
    
    # Check database
    if not check_database():
        return
    
    # Ask about superuser creation
    create_superuser()
    
    # Start the server
    start_server()

if __name__ == "__main__":
    main()

