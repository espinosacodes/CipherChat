#!/usr/bin/env python3
"""
CipherChat Web Application Starter
This script starts the Django development server for CipherChat.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Start the CipherChat web application."""
    # Get the project root directory
    project_root = Path(__file__).parent.absolute()
    
    # Activate virtual environment and start server
    venv_python = project_root / "venv_new" / "bin" / "python"
    
    if not venv_python.exists():
        print("❌ Virtual environment not found. Please run:")
        print("   python -m venv venv_new")
        print("   source venv_new/bin/activate")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Change to project directory
    os.chdir(project_root)
    
    # Start Django development server
    print("🚀 Starting CipherChat Web Application...")
    print("📍 Server will be available at: http://127.0.0.1:8000")
    print("🔐 Admin interface: http://127.0.0.1:8000/admin/")
    print("👤 Login page: http://127.0.0.1:8000/users/login/")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([str(venv_python), "manage.py", "runserver"], check=True)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
