import json
import os

from datetime import date

from django.conf.global_settings import STATICFILES_FINDERS

from kombu.utils.url import safequote

secrets_path = '/etc/secrets.json'
try:
    secrets = json.load(open(secrets_path))
except FileNotFoundError:
    secrets = {}

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
VIRTUALENV_DIR = os.path.dirname(os.path.dirname(os.path.dirname(BASE_DIR)))
VAR_DIR = os.path.join(VIRTUALENV_DIR, 'var')

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = secrets.get('django_secret', 'insecure')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'gunicorn',
    'genesis_combo_reading.apps.core'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware'
]

ROOT_URLCONF = 'genesis_combo_reading.conf.urls.main'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ]
        },
    },
]

WSGI_APPLICATION = 'genesis_combo_reading.conf.wsgi.app.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'HOST': secrets.get('db_host', 'localhost'),
        'NAME': secrets.get('db_name', 'genesis_combo_reading'),
        'USER': secrets.get('db_username', 'genesis_combo_reading'),
        'PASSWORD': secrets.get('db_password', 'changeme123')
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

CELERY_BROKER_URL = 'redis://localhost:6379/0'

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

# Logging
LOG_PATH = os.path.join(VIRTUALENV_DIR, 'var/log/django/genesis_combo_reading.log')

ADMIN = [('Gregg Keithley', 'gregg@pronym.com')]

LOGIN_URL = '/accounts/login/'
LOGOUT_URL = '/accounts/logout/'
LOGIN_REDIRECT_URL = '/dashboard/'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(VAR_DIR, 'static')
MEDIA_URL = '/uploads/'
MEDIA_ROOT = os.path.join(VAR_DIR, 'var/media')

ADMIN_MEDIA_PREFIX = '/static/admin/'

DEBUG_STATIC_FILES = True
TOKEN_EXPIRATION_MINUTES = 120
API_SECRET = secrets.get('api_secret', 'fakeapisecret123')

DEFAULT_FROM_EMAIL = 'admin@changeme.com'
USE_COMPILED_JS = False
COMPILED_JS_URL = '/packagedjs/'

ADMINS = (
    ('Gregg Keithley', 'gregg@pronym.com'),
)

MANAGERS = ADMINS

USE_TZ = True
TIME_ZONE = 'America/Chicago'

ENCRYPTION_BINARY_DIRECTORY = '/webapps/genesishealth/bin'
READING_ENCRYPTION_KEY = secrets.get('reading_encryption_key', 'abcdef1234567890')
READING_ENABLE_ENCRYPTION = False

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
