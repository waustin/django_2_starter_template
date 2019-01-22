from . base import *

DEBUG = False

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en//ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Static asset configuration
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'staticfiles')

# Upload file configuration
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'uploadfiles')

# CACHE CONFIG
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
    }
}

# EMAIL SETTINGS
EMAIL_HOST = '' # 'smtp.webfaction.com'
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
DEFAULT_FROM_EMAIL = ''
SERVER_EMAIL = ''
