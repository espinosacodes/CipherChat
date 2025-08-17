"""
ASGI config for CipherChat web application.
"""

import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cipherchat_web.settings')

application = get_asgi_application()

