"""
Django settings for {{ project_name }} project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
import sys
import dj_database_url
import logging

PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
BASE_DIR = os.path.dirname(PROJECT_DIR)

# App/Library Paths
sys.path.append(os.path.join(BASE_DIR, 'apps'))

# Users TO EMAIL Errors to based on LOGGING Settings
ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)
MANAGERS = ADMINS


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '6l)+-$^dh#d@lsp+agphlf94%ipya$d50j!$dq_yn9pk67&!*7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',

    # Grappelli and Filebrowser Admin - must come before the admin
    'filebrowser',
    'django.contrib.admin',

    # 3rd Party
    'mptt',
    'django_extensions',
    'sitetree',
    'my_sitetree_changes',  # my custom overrides to make editing simpler
    'easy_thumbnails',

    # our apps
    'text_blocks',
    'pages',
    'promotions',
    'blog',


)

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{{ project_name }}.urls'

WSGI_APPLICATION = '{{ project_name }}.wsgi.application'


# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = False

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = False


# Upload Media
# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'uploadfiles')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/uploads/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'staticfiles')

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, 'assets'),
)

# Template Settings
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

# DATABASE Configured by URL
DATABASES = {'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))}

# CONNECTION MAX AGE
CONN_MAX_AGE = 60 * 5  # keep db connections open for 5 minutes

# SUPPRESS FACTORY BOY LOGGING MESSAGES
logging.getLogger("factory").setLevel(logging.WARN)


## TESTING
# must add django_nose as the first installed app so that coverage can correctly run
INSTALLED_APPS = ('django_nose',) + INSTALLED_APPS

# Use nose to run all tests
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# UN-COMMENT TO SET NOSE TESTING ARGUMENTS, INCLUDING COVERAGE
# NOSE_ARGS = [
#    '--with-coverage',
#    '--cover-package=pages,text_blocks',
# ]

# APP SETTINGS


FILEBROWSER_SHOW_IN_DASHBOARD = False

# FILEBROWSER SETTINGS
FILEBROWSER_DIRECTORY = ''

FILEBROWSER_NORMALIZE_FILENAME = True

# Allow FileBrowser Extensions
FILEBROWSER_EXTENSIONS = {
    'Folder': [''],
    'Image': ['.jpg', '.jpeg', '.gif', '.png'],
    'Document': ['.pdf', '.txt', '.doc', '.rtf', '.xls'],
    'Audio': ['.mp3'],
    'Video': ['.mp4']
}
FILEBROWSER_VERSIONS_BASEDIR = '_versions'

FILEBROWSER_VERSIONS = {
    'admin_thumbnail': {'verbose_name': 'Admin Thumbnail', 'width': 60, 'height': 60, 'opts': 'crop upscale'},
    'thumbnail': {'verbose_name': 'Thumbnail (100px) Square', 'width': 100, 'height': 100, 'opts': 'crop'},
    'small': {'verbose_name': 'Small (200px Wide)', 'width': 200, 'height': '', 'opts': ''},
    'medium': {'verbose_name': 'Medium (400px Wide)', 'width': 400, 'height': '', 'opts': ''},
    'big': {'verbose_name': 'Big (600px Wide)', 'width': 600, 'height': '', 'opts': ''},
    'large': {'verbose_name': 'Large (800px Wide)', 'width': 800, 'height': '', 'opts': ''},
}

# EASY THUMBNAILS
THUMBNAIL_SUBDIR = '_thumbs'

# APP SETTINGS
PAGES_HEADER_IMAGE_DIR = 'page_headers'

# PROMOTIONS
PROMOTIONS_BANNER_IMAGE_DIR = 'banners'

# BLOG
BLOG_POST_THUMB_DIR = 'blog/thumbs'
POSTS_PER_PAGE = 10
