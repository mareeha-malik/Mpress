"""
Django settings for mpress project.
"""

from pathlib import Path
import os
import sys
from dotenv import load_dotenv
import cloudinary

# =========================
# BASE CONFIG
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()

SECRET_KEY = os.environ.get(
    'SECRET_KEY',
    'django-insecure-dg-_q)qiuntp&aztqohlqh$)3v%26o^r0*c3%gpm%c+&+wdh$k'
)

DEBUG = os.environ.get('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = [
    "mpress.onrender.com",
    ".onrender.com",
    "localhost",
    "127.0.0.1"
]

# =========================
# CLOUDINARY CONFIG
# =========================
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

# =========================
# TEST SETTINGS (IMPORTANT)
# =========================
if 'test' in sys.argv:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        }
    }

# =========================
# INSTALLED APPS (FIXED)
# =========================
INSTALLED_APPS = [
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Third-party
    'cloudinary',
    'cloudinary_storage',

    # Local apps (use full AppConfig path to ensure ready() is called)
    'accounts.apps.AccountsConfig',
    'blog.apps.BlogConfig',
]

# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mpress.urls'

# =========================
# TEMPLATES
# =========================
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'blog.context_processors.sidebar_data',
            ],
        },
    },
]

WSGI_APPLICATION = 'mpress.wsgi.application'

# =========================
# DATABASE
# =========================
# Support DATABASE_URL for CI/production environments (e.g., postgres://user:pass@host:port/dbname)
# Fall back to SQLite for local development
database_url = os.environ.get('DATABASE_URL')

if database_url:
    # Use dj-database-url if available, otherwise parse manually
    try:
        import dj_database_url
        DATABASES = {'default': dj_database_url.config(default=database_url, conn_max_age=600)}
    except Exception:
        # Manual parsing for postgres URLs
        if 'postgres' in (database_url or '') or 'postgresql' in (database_url or ''):
            from urllib.parse import urlparse
            parsed = urlparse(database_url)
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.postgresql',
                    'NAME': parsed.path.lstrip('/'),
                    'USER': parsed.username,
                    'PASSWORD': parsed.password,
                    'HOST': parsed.hostname,
                    'PORT': parsed.port or 5432,
                }
            }
        else:
            DATABASES = {
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': BASE_DIR / 'db.sqlite3',
                }
            }
else:
    # Local development defaults to SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# When running tests in CI, prefer an isolated SQLite database to avoid
# test flakiness caused by service health checks or network issues. This
# also guarantees DATABASES always contains an ENGINE value during tests.
if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'test_db.sqlite3',
        }
    }

# =========================
# AUTH PASSWORD VALIDATORS
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================
# INTERNATIONALIZATION
# =========================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# =========================
# STATIC FILES
# =========================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# =========================
# STORAGES (Production)
# =========================
STORAGES = {
    'default': {
        'BACKEND': 'cloudinary_storage.storage.MediaCloudinaryStorage',
    },
    'staticfiles': {
        'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
    },
}

# =========================
# MEDIA FILES
# =========================
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# =========================
# SECURITY & HOSTING
# =========================
CSRF_TRUSTED_ORIGINS = [
    'https://mpress.onrender.com',
]
