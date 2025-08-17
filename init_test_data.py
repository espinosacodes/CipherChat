#!/usr/bin/env python3
"""
Script to initialize test data for CipherChat web application.
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    """Initialize test data for CipherChat."""
    # Get the project root directory
    project_root = Path(__file__).parent.absolute()
    
    # Activate virtual environment
    venv_python = project_root / "venv_new" / "bin" / "python"
    
    if not venv_python.exists():
        print("❌ Virtual environment not found. Please run:")
        print("   python -m venv venv_new")
        print("   source venv_new/bin/activate")
        print("   pip install -r requirements.txt")
        sys.exit(1)
    
    # Change to project directory
    os.chdir(project_root)
    
    print("🚀 Initializing CipherChat Test Data...")
    print("This will create:")
    print("- 5 test users with encryption keys")
    print("- 10 encrypted messages between users")
    print("- Key exchanges and security logs")
    print("- All necessary data for testing the application")
    print("-" * 50)
    
    try:
        # Run the Django management command
        result = subprocess.run([
            str(venv_python), 
            "manage.py", 
            "init_test_data",
            "--users", "5",
            "--messages", "10"
        ], check=True, capture_output=True, text=True)
        
        print(result.stdout)
        
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
        
        print("\n✅ Test data initialization completed successfully!")
        print("\n📋 Test User Credentials:")
        print("Username: testuser1, Password: testpass123")
        print("Username: testuser2, Password: secure456")
        print("Username: testuser3, Password: password789")
        print("Username: testuser4, Password: secret101")
        print("Username: testuser5, Password: cipher202")
        print("\n🌐 You can now test the application at: http://127.0.0.1:8000/")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error initializing test data: {e}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n🛑 Test data initialization cancelled by user")
        sys.exit(1)

if __name__ == "__main__":
    main()
