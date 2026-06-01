"""
WSGI config for Smart ID Card Scan Website.

It exposes the WSGI callable as a module-level variable named ``application``.
"""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smartid.settings')

application = get_wsgi_application()
