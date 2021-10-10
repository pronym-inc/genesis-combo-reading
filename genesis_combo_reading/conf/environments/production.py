from genesis_combo_reading.conf.generic.settings import *  # noqa


DEBUG = False
DEBUG_STATIC_FILES = False

ALLOWED_HOSTS = ['gcr.pronym.com']

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'rotating_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_PATH,
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5
        }
    },
    'loggers': {
        'django': {
            'handlers': ['rotating_file'],
            'level': 'WARNING',
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        }
    }
}

