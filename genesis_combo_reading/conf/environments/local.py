from genesis_combo_reading.conf.generic.settings import *  # noqa


DEBUG = True
DEBUG_STATIC_FILES = True

ALLOWED_HOSTS = ['*']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': True,
        }
    }
}

ENCRYPTION_BINARY_DIRECTORY = '/Users/greggkeithley/Work/Genesis/genesis-combo-reading/venv/bin'
