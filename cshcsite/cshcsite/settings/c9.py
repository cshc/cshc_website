""" Django settings for cshcsite project - Cloud9 development environment
"""

from cshcsite.settings.base import *

ALLOWED_HOSTS = ['127.0.0.1', 'cshc-website-cshc.c9.io']

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

########## DATABASE CONFIGURATION
#See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'c9',
        'USER': 'cshc',
        'PASSWORD': '', #get_env_setting('DB_PASSWORD'),
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}

# Only specify this option for syncdb or migrate calls (for efficiency)
# Ref: Comment on http://stackoverflow.com/a/5270072
import sys
if 'migrate' in sys.argv or 'syncdb' in sys.argv:
    DATABASES['default']['OPTIONS'] = {'init_command': 'SET storage_engine=MyISAM',}

########## TOOLBAR CONFIGURATION
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INSTALLED_APPS += (
    'debug_toolbar',
    'django_extensions',
)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INTERNAL_IPS = ('127.0.0.1',)

# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
MIDDLEWARE_CLASSES += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

DEBUG_TOOLBAR_CONFIG = {
    #'INTERCEPT_REDIRECTS': False,
}
########## END TOOLBAR CONFIGURATION

########## TEST SETTINGS
TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = SITE_ROOT
TEST_DISCOVER_ROOT = SITE_ROOT
TEST_DISCOVER_PATTERN = "test_*.py"


########## django-disqus CONFIGURATION

DISQUS_WEBSITE_SHORTNAME = 'cshc-c9'

########## END django-disqus CONFIGURATION
