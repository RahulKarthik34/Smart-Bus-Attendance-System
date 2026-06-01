"""
Smart ID Card Scan Website - Django Settings
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from .env file
load_dotenv(BASE_DIR / '.env')

# =====================================================
# Core Settings
# =====================================================

SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-smartid-dev-key-change-in-production')

DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'

ALLOWED_HOSTS = ['*']

# =====================================================
# Application Configuration
# =====================================================

APP_NAME = os.getenv('APP_NAME', 'Smart ID Card Scan Website')
APP_VERSION = os.getenv('APP_VERSION', '1.0.0')

# =====================================================
# Scan Configuration
# =====================================================

ALLOWED_SCAN_TYPES = ['barcode', 'manual']
SCAN_START_TIME = '00:00'
SCAN_END_TIME = '23:59'
CLEANUP_TIME = '18:00'
ALLOWED_ROLES = ['student', 'admin']
SKIP_TIME_CHECK = os.getenv('SKIP_TIME_CHECK', 'True').lower() == 'true'

# =====================================================
# Installed Applications
# =====================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'rest_framework',
    'corsheaders',
    # Local apps
    'attendance',
]

# =====================================================
# Middleware
# =====================================================

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be before CommonMiddleware
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# =====================================================
# CORS Configuration
# =====================================================

CORS_ALLOWED_ORIGINS = [
    'http://localhost:8080',
    'http://127.0.0.1:8080',
    'http://localhost:3000',
    'http://127.0.0.1:3000',
]

# Allow all origins in development
CORS_ALLOW_ALL_ORIGINS = DEBUG

CORS_ALLOW_CREDENTIALS = True

# =====================================================
# URL Configuration
# =====================================================

ROOT_URLCONF = 'smartid.urls'

# =====================================================
# Templates
# =====================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# =====================================================
# WSGI
# =====================================================

WSGI_APPLICATION = 'smartid.wsgi.application'

# =====================================================
# Database Configuration (MySQL)
# =====================================================

DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': os.getenv('DB_NAME', 'attendance_system'),
        'USER': os.getenv('DB_USER', 'root'),
        'PASSWORD': os.getenv('DB_PASSWORD', '') or '342517',
        'HOST': os.getenv('DB_HOST', '127.0.0.1'),
        'PORT': os.getenv('DB_PORT', '3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
            'autocommit': True,
            'raise_on_warnings': True,
        },
    }
}

# =====================================================
# Django REST Framework Configuration
# =====================================================

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],
    'EXCEPTION_HANDLER': 'attendance.views.custom_exception_handler',
}

# =====================================================
# Internationalization
# =====================================================

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'
USE_I18N = True
USE_TZ = False  # Using naive datetimes to match existing schema

# =====================================================
# Static files
# =====================================================

STATIC_URL = 'static/'

# =====================================================
# Default primary key field type
# =====================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
