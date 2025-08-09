# 🚀 CipherChat Installation Guide

This guide provides detailed installation instructions for CipherChat on different operating systems and environments.

## 📋 Prerequisites

- **Python 3.7+** (3.8 or higher recommended)
- **pip** (Python package installer)
- **Git** (for cloning the repository)

## 🔧 Quick Installation

### Option 1: Automated Setup (Recommended)

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd CipherChat
   ```

2. **Run the setup script:**
   ```bash
   python setup.py
   ```

This will automatically:
- Check Python version compatibility
- Create a virtual environment
- Install all dependencies
- Create necessary directories
- Test the installation

### Option 2: Manual Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd CipherChat
   ```

2. **Create virtual environment (recommended):**
   ```bash
   python -m venv cipherchat_env
   ```

3. **Activate virtual environment:**
   
   **On Linux/macOS:**
   ```bash
   source cipherchat_env/bin/activate
   ```
   
   **On Windows:**
   ```cmd
   cipherchat_env\Scripts\activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Test installation:**
   ```bash
   python demo.py
   ```

## 🖥️ Platform-Specific Instructions

### 🐧 Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Python and pip if not already installed
sudo apt install python3 python3-pip python3-venv git

# Clone and setup CipherChat
git clone <repository-url>
cd CipherChat
python3 setup.py
```

### 🍎 macOS

```bash
# Install Homebrew if not already installed
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python
brew install python git

# Clone and setup CipherChat
git clone <repository-url>
cd CipherChat
python3 setup.py
```

### 🪟 Windows

1. **Install Python from [python.org](https://www.python.org/downloads/)**
   - Make sure to check "Add Python to PATH" during installation

2. **Install Git from [git-scm.com](https://git-scm.com/download/win)**

3. **Open Command Prompt or PowerShell and run:**
   ```cmd
   git clone <repository-url>
   cd CipherChat
   python setup.py
   ```

### 🐳 Docker (Optional)

Create a Docker container for CipherChat:

1. **Create Dockerfile:**
   ```dockerfile
   FROM python:3.9-slim
   
   WORKDIR /app
   COPY . .
   
   RUN pip install -r requirements.txt
   
   CMD ["python", "cipherchat.py"]
   ```

2. **Build and run:**
   ```bash
   docker build -t cipherchat .
   docker run -it cipherchat
   ```

## 🔍 Verification

After installation, verify CipherChat is working correctly:

### 1. Run Demo
```bash
python demo.py
```

Expected output: Successfully demonstrates encryption, decryption, and security features.

### 2. Test Interactive Mode
```bash
python cipherchat.py
```

Expected output: CipherChat main menu appears.

### 3. Test Programmatic Usage
```python
from src.key_manager import KeyManager
from src.secure_channel import SecureChannel

key_manager = KeyManager()
print("✅ CipherChat modules imported successfully")
```

## 🔧 Troubleshooting

### Common Issues

**1. ModuleNotFoundError: No module named 'cryptography'**
```bash
# Solution: Activate virtual environment and reinstall
source cipherchat_env/bin/activate  # or cipherchat_env\Scripts\activate on Windows
pip install -r requirements.txt
```

**2. Permission denied errors on Linux/macOS**
```bash
# Solution: Use virtual environment instead of system-wide installation
python3 -m venv cipherchat_env
source cipherchat_env/bin/activate
pip install -r requirements.txt
```

**3. Python version too old**
```bash
# Check Python version
python --version

# Install newer Python version if needed
# Ubuntu: sudo apt install python3.9
# macOS: brew install python@3.9
# Windows: Download from python.org
```

**4. SSL/TLS certificate errors**
```bash
# Solution: Update certificates or use trusted hosts
pip install --trusted-host pypi.org --trusted-host pypi.python.org -r requirements.txt
```

### 🔍 Environment Issues

**Externally Managed Environment (Modern Linux)**
```bash
# Create virtual environment (recommended approach)
python3 -m venv cipherchat_env
source cipherchat_env/bin/activate
pip install -r requirements.txt
```

**WSL (Windows Subsystem for Linux)**
```bash
# Make sure you're in the correct directory
cd /mnt/c/Users/[YourUsername]/Desktop/CipherChat
python3 -m venv cipherchat_env
source cipherchat_env/bin/activate
pip install -r requirements.txt
```

## 📦 Dependencies Explained

| Package | Version | Purpose |
|---------|---------|---------|
| `cryptography` | >=41.0.0 | Core cryptographic operations (RSA, AES, signatures) |
| `pycryptodome` | >=3.19.0 | Additional crypto utilities and algorithms |
| `colorama` | >=0.4.6 | Cross-platform colored terminal output |

## 🏗️ Development Setup

For developers who want to contribute:

```bash
# Clone with development dependencies
git clone <repository-url>
cd CipherChat

# Create development environment
python -m venv dev_env
source dev_env/bin/activate  # or dev_env\Scripts\activate on Windows

# Install with development extras
pip install -r requirements.txt
pip install pytest black flake8 mypy  # Optional: development tools

# Run tests
python -m pytest tests/  # If tests exist

# Code formatting
black src/
flake8 src/
```

## 🆘 Getting Help

If you encounter issues:

1. **Check the [README.md](README.md)** for usage instructions
2. **Run the demo** to verify installation: `python demo.py`
3. **Check Python version**: Must be 3.7+
4. **Verify virtual environment** is activated
5. **Try reinstalling** dependencies: `pip install --force-reinstall -r requirements.txt`

## 🔄 Updating CipherChat

To update to the latest version:

```bash
cd CipherChat
git pull origin main
pip install --upgrade -r requirements.txt
python demo.py  # Test updated version
```

---

**🔐 Happy secure messaging with CipherChat!**
