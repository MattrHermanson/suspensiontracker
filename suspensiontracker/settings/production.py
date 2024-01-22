from .base import *

ALLOWED_HOSTS = ['suspensiontracker.com', 'www.suspensiontracker.com']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'suspensiontrackerdb',
        'USER': 'mattrhermanson',
        'PASSWORD': 'Matt90001*',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

STATIC_ROOT = '/home/mattrhermanson/apps/mystatic'
STATIC_URL = '/static/'

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL')
SERVER_EMAIL = os.environ.get('SEVER_EMAIL')
EMAIL_HOST = os.environ.get('EMAIL_HOST')

EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
EMAIL_PORT = 587