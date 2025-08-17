# CipherChat Web Application

A secure, end-to-end encrypted messaging web application built with Django, featuring RSA + AES hybrid encryption, digital signatures, and secure key exchange.

## 🚀 Features

### Security Features
- **End-to-End Encryption**: Messages are encrypted with RSA + AES hybrid encryption
- **Digital Signatures**: All messages are digitally signed for authentication
- **Tamper-Proof Messages**: Cryptographic verification ensures message integrity
- **Secure Key Exchange**: Safe public key distribution and management
- **Forward Secrecy**: Each message uses unique encryption keys

### Web Interface Features
- **Modern UI**: Beautiful, responsive design with Bootstrap 5
- **User Management**: Secure user registration and authentication
- **Dashboard**: Comprehensive overview of messages, keys, and security status
- **Message Management**: Send, receive, and view encrypted messages
- **Key Management**: Generate, import, and export cryptographic keys
- **Security Logging**: Detailed audit trail of all security operations

## 🛠️ Technology Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (configurable for production)
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Cryptography**: Python cryptography library
- **Authentication**: Django built-in user authentication
- **Forms**: Django Crispy Forms with Bootstrap styling

## 📋 Prerequisites

- Python 3.8+
- pip (Python package installer)
- Virtual environment (recommended)

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd CipherChat
```

### 2. Create Virtual Environment
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables
Create a `.env` file in the project root:
```env
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### 5. Run Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)
```bash
python manage.py createsuperuser
```

### 7. Run the Development Server
```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

## 🏗️ Project Structure

```
CipherChat/
├── cipherchat_web/          # Django project settings
│   ├── settings.py          # Main Django configuration
│   ├── urls.py             # Main URL routing
│   ├── wsgi.py             # WSGI application
│   └── asgi.py             # ASGI application
├── chat/                    # Chat application
│   ├── models.py           # Database models
│   ├── views.py            # View logic
│   ├── forms.py            # Form definitions
│   ├── urls.py             # Chat URL routing
│   └── admin.py            # Admin interface
├── users/                   # User management application
│   ├── models.py           # User models
│   ├── views.py            # User views
│   ├── forms.py            # User forms
│   └── urls.py             # User URL routing
├── templates/               # HTML templates
│   ├── base.html           # Base template
│   ├── chat/               # Chat templates
│   └── users/              # User templates
├── static/                  # Static files (CSS, JS, images)
├── media/                   # User-uploaded files
├── keys/                    # Cryptographic keys storage
├── messages/                # Encrypted message storage
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── README_WEB.md           # This file
```

## 🔐 Security Architecture

### Cryptographic Implementation
1. **Key Generation**: 2048-bit RSA key pairs for each user
2. **Message Encryption**: 
   - Generate random AES-256 key for each message
   - Encrypt message content with AES key
   - Encrypt AES key with recipient's RSA public key
   - Sign message with sender's RSA private key
3. **Message Decryption**:
   - Decrypt AES key with recipient's RSA private key
   - Decrypt message content with AES key
   - Verify digital signature with sender's public key

### Security Features
- **Session Security**: Secure session cookies with HTTP-only flags
- **CSRF Protection**: Built-in Django CSRF protection
- **XSS Protection**: Security headers and input validation
- **SQL Injection Protection**: Django ORM with parameterized queries
- **File Upload Security**: File type and size validation

## 📱 Usage Guide

### 1. User Registration
- Navigate to `/users/register/`
- Fill in your details and create an account
- You'll be automatically logged in

### 2. Generate Cryptographic Keys
- After registration, go to `/chat/keys/generate/`
- Generate your RSA key pair for encryption
- This is required before sending messages

### 3. Import Recipient Keys
- Go to `/chat/keys/import/`
- Enter the username and public key of the person you want to message
- You need their public key to send encrypted messages

### 4. Send Encrypted Messages
- Navigate to `/chat/send/`
- Enter recipient username and message content
- Your message will be automatically encrypted and sent

### 5. View and Decrypt Messages
- Go to `/chat/messages/` to see all your messages
- Click on a message to decrypt and view its content
- Messages are automatically marked as read when viewed

## 🔧 Configuration

### Production Settings
For production deployment, update your `.env` file:
```env
DEBUG=False
SECRET_KEY=your-production-secret-key
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### Database Configuration
The default configuration uses SQLite. For production, consider PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'cipherchat_db',
        'USER': 'db_user',
        'PASSWORD': 'db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🚀 Deployment

### Using Gunicorn (Recommended)
```bash
pip install gunicorn
gunicorn cipherchat_web.wsgi:application --bind 0.0.0.0:8000
```

### Using Docker
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "cipherchat_web.wsgi:application", "--bind", "0.0.0.0:8000"]
```

### Using Heroku
```bash
heroku create your-cipherchat-app
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False
git push heroku main
```

## 🧪 Testing

### Run Tests
```bash
python manage.py test
```

### Run with Coverage
```bash
pip install coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## 🔍 Monitoring and Logging

### Security Logs
All security-related operations are logged to the database:
- Key generation and import
- Message sending and receiving
- User authentication
- Security checks and validations

### Admin Interface
Access `/admin/` to view:
- User profiles and cryptographic keys
- Message metadata and encryption status
- Security logs and audit trails
- Key exchange records

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## ⚠️ Security Considerations

### Important Notes
- **Private Keys**: Never share your private keys with anyone
- **Public Keys**: Only share public keys through secure channels
- **Key Verification**: Verify public keys through trusted channels
- **Regular Updates**: Keep dependencies updated for security patches

### Limitations
- This is a demonstration application
- For production use, consider additional security measures
- Regular security audits are recommended
- Consider using hardware security modules (HSM) for key storage

## 🆘 Support

For issues and questions:
1. Check the existing issues in the repository
2. Review the security documentation
3. Create a new issue with detailed information

## 🔮 Future Enhancements

- **Real-time Messaging**: WebSocket support for instant messaging
- **File Encryption**: Secure file sharing with encryption
- **Group Chats**: Encrypted group messaging
- **Mobile App**: Native mobile applications
- **Advanced Key Management**: Key rotation and revocation
- **Audit Logging**: Enhanced security monitoring

---

**Remember**: Security is a continuous process. Regularly review and update your security practices.

