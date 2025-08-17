"""
WSGI config for CipherChat web application.
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cipherchat_web.settings')

application = get_wsgi_application()

