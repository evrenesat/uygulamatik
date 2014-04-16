# -*-  coding: utf-8 -*-
# Django settings for uygulamatik project.


import os

DEVELOPMENT_MODE = True
BASEDIR = os.path.dirname(__file__) + '/../'

CKEDITOR_UPLOAD_PATH = BASEDIR + 'media/uploads'

LOCALE_PATHS = [BASEDIR + 'locale', ]

ADMINS = (
    ('Evren Esat Ozkan', 'eeo@elipsis.com.tr'),
    ('Yalcin Ozveren', 'yalcinozveren@elipsis.com.tr'),
    ('M.Ozgur Bayhan', 'mozgurbayhan@elipsis.com.tr'),
)
EMAIL_HOST = 'smtp.webfaction.com'
EMAIL_HOST_USER = 'appserver'
EMAIL_HOST_PASSWORD = 'a1q1a1q1'
DEFAULT_FROM_EMAIL = 'appserver@post.uygulamatik.com'
SERVER_EMAIL = 'appserver@post.uygulamatik.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_SUBJECT_PREFIX = '[UMATiK] '

#DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
#        'NAME': 'uygulamatik',                      # Or path to database file if using sqlite3.
#        'USER': 'uygulamatik',                      # Not used with sqlite3.
#        'PASSWORD': '1234',                  # Not used with sqlite3.
#        'HOST': 'localhost',                      # Set to empty string for localhost. Not used with sqlite3.
#        'PORT': '5432',                      # Set to empty string for default. Not used with sqlite3.
#    }
#}
#DEBUG = True
#TEMPLATE_DEBUG = DEBUG

APPSERVERURL = 'http://appserver.uygulamatik.com/'

MANAGERS = ADMINS
DEFAULT_FILE_STORAGE = 'umatik.models.ASCIIFileSystemStorage'

SESSION_ENGINE = 'redis_sessions.session'

SESSION_REDIS_HOST = 'localhost'
SESSION_REDIS_PORT = 6379
SESSION_REDIS_DB = 0

MESSAGE_STORAGE = 'django.contrib.messages.storage.cookie.CookieStorage'
# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'Europe/Istanbul'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'tr'
LANGUAGES = (('tr', u'Türkçe'), ('en', 'English'), ('de', 'Deutsch'))
SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"
MEDIA_ROOT = BASEDIR + '/media/'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = BASEDIR + '/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.

)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'lu1%46yrk!sjgq8f^)7^h*kj5spo8-uitubwt$@os!_vt^t$ig'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'localeurl.middleware.LocaleURLMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.contrib.sessions.middleware.SessionMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # 'middleware.dil.MultilingualURLMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',

)
TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.debug",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.tz",
    "django.core.context_processors.request",
    "django.contrib.messages.context_processors.messages",
    'umatik.preprocessors.available_languages',
)

ROOT_URLCONF = 'uygulamatik.urls'

TEMPLATE_DIRS = (BASEDIR + '/templates',)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'easy_thumbnails',
    'django.contrib.admin',
    'umatik',
    'south',
    'blok',
    'ckeditor',
    'admin_tabs',
    'mptt',
    'treeadmin',
    'localeurl',
    'at_shop_order',
    'qurl'
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
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

CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True
CACHE_MIDDLEWARE_KEY_PREFIX = 'ghh'
CACHE_MIDDLEWARE_SECONDS = 99999
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        #        'LOCATION': 'unix:/home/sleytr/memcached.sock',
    }
}

CKEDITOR_MEDIA_URL = '/media'
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            ['Undo', 'Redo',
             '-', 'Bold', 'Italic', 'Underline',
             '-', 'Link', 'Unlink', 'Anchor',
             '-', 'Format',
             '-', 'SpellChecker', 'Scayt',
             '-', 'Maximize', ],
            ['HorizontalRule',
             '-', 'Table',
             '-', 'BulletedList', 'NumberedList',
             '-', 'Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord',
             '-', 'SpecialChar',
             '-', 'Source',
             '-', 'About',
            ]
        ],
        'width': 840,
        'height': 300,
        'toolbarCanCollapse': False,
    }
}
from local_settings import *


AUTHENTICATION_BACKENDS = [
    'umatik.email_backend.EmailBackend'
]
LOCALE_INDEPENDENT_PATHS = [
    '/api1/*',
    '/getappid/*',
    '/9oo/*',
    '/app/*.html',
    '/app/js/*',
    '/app/css/*',
    '/admin/get_app_map*',
    '/admin/right_click_context*',
    '/admin/get_node_form*',
    '/admin/add_node*',
    '/admin/delete_node*',
    '/admin/update_node*',
    '/admin/get_nodes*',
    '/admin/get_node_update_form*',
    '/admin/get_store_list*',
    '/admin/get_exhibitor_list*',
    '/admin/get_neighbours*',
    '/admin/add_neighbour*',
    # '/admin/*',
    # '/admin/*',
    # '/admin/*',
]
