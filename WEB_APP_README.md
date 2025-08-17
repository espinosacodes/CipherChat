# CipherChat Web Application

A secure Django-based web application for encrypted messaging.

## Quick Start

### Option 1: Using the starter script (Recommended)
```bash
./start_web_app.py
```

### Option 2: Manual start
```bash
# Activate virtual environment
source venv_new/bin/activate

# Start Django development server
python manage.py runserver
```

## Access URLs

- **Main Application**: http://127.0.0.1:8000/
- **Login Page**: http://127.0.0.1:8000/users/login/
- **Admin Interface**: http://127.0.0.1:8000/admin/
- **Registration**: http://127.0.0.1:8000/users/register/

## Features

- ✅ User authentication and registration
- ✅ Secure encrypted messaging
- ✅ Key management
- ✅ Message encryption/decryption
- ✅ Admin interface
- ✅ Bootstrap 5 UI with crispy forms

## Security Features

- CSRF protection
- XSS protection
- Content Security Policy
- Secure session handling
- File upload validation
- Input sanitization

## Development

### Prerequisites
- Python 3.8+
- Virtual environment

### Setup
```bash
# Create virtual environment
python -m venv venv_new

# Activate virtual environment
source venv_new/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations (if needed)
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### Testing
```bash
# Check for issues
python manage.py check

# Run tests
python manage.py test
```

## Project Structure

```
CipherChat/
├── cipherchat_web/     # Django project settings
├── chat/              # Main chat application
├── users/             # User authentication app
├── templates/         # HTML templates
├── static/           # Static files (CSS, JS)
├── media/            # User uploaded files
├── keys/             # Encryption keys
├── messages/         # Encrypted messages
└── venv_new/         # Virtual environment
```

## Troubleshooting

### Virtual Environment Issues
If you get "externally-managed-environment" errors:
```bash
# Create a new virtual environment
python -m venv venv_new --clear
source venv_new/bin/activate
pip install -r requirements.txt
```

### Database Issues
```bash
# Reset database (WARNING: This will delete all data)
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

### Port Already in Use
If port 8000 is already in use:
```bash
python manage.py runserver 8001
```

## Security Notes

- This is a development server. For production, use a proper WSGI server like Gunicorn
- Change the SECRET_KEY in production
- Set DEBUG=False in production
- Use HTTPS in production
- Regularly update dependencies for security patches
