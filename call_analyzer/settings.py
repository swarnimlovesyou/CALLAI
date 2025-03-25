"""
Django settings for call_analyzer project.

Generated by 'django-admin startproject' using Django 5.1.7.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-d7x)u$lxzhjjkk-gtddw(vhht*@es#od1ys5_ysyoov*+hha9j')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'

# Get host names from environment variable
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', '').split(',')

# CORS settings for development
CORS_ALLOW_ALL_ORIGINS = True if DEBUG else False
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = os.getenv('CORS_ALLOWED_ORIGINS', '').split(',')

# Additional CORS settings for development
if DEBUG:
    CORS_ALLOW_METHODS = [
        'DELETE',
        'GET',
        'OPTIONS',
        'PATCH',
        'POST',
        'PUT',
    ]
    CORS_ALLOW_HEADERS = [
        'accept',
        'accept-encoding',
        'authorization',
        'content-type',
        'dnt',
        'origin',
        'user-agent',
        'x-csrftoken',
        'x-requested-with',
    ]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third-party apps
    'rest_framework',
    'rest_framework.authtoken',  # Add token authentication
    'corsheaders',  # Add CORS headers
    'debug_toolbar',  # Add debug toolbar
    
    # Local apps
    'analyzer',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # Add CORS middleware (must be before CommonMiddleware)
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',  # Add debug toolbar middleware
]

# For local development, allow all origins if in DEBUG mode
if DEBUG:
    CORS_ALLOW_ALL_ORIGINS = True

# Add production frontend URL from environment variable
frontend_url = os.environ.get('FRONTEND_URL')
if frontend_url:
    CORS_ALLOWED_ORIGINS.append(frontend_url)

# Handle Render.com deployment
if '.onrender.com' in ''.join(ALLOWED_HOSTS):
    CORS_ALLOWED_ORIGINS.extend([
        "https://ai-call-analyzer-frontend.onrender.com",
    ])
    CSRF_TRUSTED_ORIGINS.extend([
        "https://ai-call-analyzer-frontend.onrender.com",
    ])

# CSRF Configuration
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

INTERNAL_IPS = [
    '127.0.0.1',
]

ROOT_URLCONF = 'call_analyzer.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
            os.path.join(BASE_DIR, 'frontend/.next'),
        ],
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

WSGI_APPLICATION = 'call_analyzer.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

# Ensure database is configured via dj-database-url
import dj_database_url
DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend/.next/static'),
]

# Media files (User uploads)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# API Keys
ASSEMBLY_AI_API_KEY = os.getenv('ASSEMBLY_AI_API_KEY')
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}
