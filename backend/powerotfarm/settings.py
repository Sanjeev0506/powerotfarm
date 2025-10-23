import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(str(BASE_DIR / '.env'))

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY', 'dev-secret-key')
DEBUG = os.getenv('DJANGO_DEBUG', 'True') == 'True'

ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '*').split(',')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'apps.contact',
    'apps.orders',
    'apps.payments',
    'apps.core',
]

MIDDLEWARE = [
    # corsheaders should be high in the middleware stack
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'powerotfarm.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'powerotfarm.wsgi.application'

# Database
DATABASES = {}

if os.getenv('MYSQL_HOST'):
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE'),
        'USER': os.getenv('MYSQL_USER'),
        'PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'HOST': os.getenv('MYSQL_HOST'),
        'PORT': os.getenv('MYSQL_PORT', '3306'),
        'OPTIONS': {'charset': 'utf8mb4'},
    }
else:
    # fallback to sqlite for easy local dev
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# CORS settings - default to permissive in DEBUG; set env var DJANGO_CORS_ALLOW_ALL=False to restrict
CORS_ALLOW_ALL_ORIGINS = os.getenv('DJANGO_CORS_ALLOW_ALL', 'True') == 'True' if DEBUG else os.getenv('DJANGO_CORS_ALLOW_ALL', 'False') == 'True'
if not CORS_ALLOW_ALL_ORIGINS:
    # allow a configured list if provided
    raw = os.getenv('DJANGO_CORS_ALLOWED_ORIGINS', '')
    CORS_ALLOWED_ORIGINS = [s.strip() for s in raw.split(',') if s.strip()]
# serve additional static files from the frontend directory during development
STATICFILES_DIRS = [
    BASE_DIR.parent / 'frontend',
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email settings - use env
EMAIL_BACKEND = os.getenv('EMAIL_BACKEND', 'django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = os.getenv('EMAIL_HOST', '')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', '')
EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True') == 'True'
DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL', 'webmaster@localhost')
CONTACT_NOTIFICATION_EMAIL = os.getenv('CONTACT_NOTIFICATION_EMAIL', 'info@powerotfarms.com')
