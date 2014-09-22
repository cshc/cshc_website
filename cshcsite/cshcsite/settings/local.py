# Django settings for cshcsite project - local development environment


from base import *

ALLOWED_HOSTS = ['127.0.0.1']

########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG

TEMPLATE_STRING_IF_INVALID = '######'
########## END DEBUG CONFIGURATION

MEDIA_ROOT = normpath(join(SITE_ROOT, 'media'))
MEDIA_URL = '/media/'
STATIC_ROOT = normpath(join(SITE_ROOT, 'assets'))
STATIC_URL = '/static/'

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

########## EMAIL CONFIGURATION
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'cshc.club@gmail.com'
EMAIL_HOST_PASSWORD = get_env_setting('EMAIL_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
########## END EMAIL CONFIGURATION

########## END EMAIL CONFIGURATION


########## DATABASE CONFIGURATION
#See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.sqlite3',
       'NAME': normpath(join(DJANGO_ROOT, '..', '..', '..', 'cshc.db')),
       'USER': '',
       'PASSWORD': '',
       'HOST': '',
       'PORT': '',
   }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'test',
#         'USER': 'root',
#         'PASSWORD': '',
#         'HOST': '',
#         'PORT': '',
#     }
# }

########## END DATABASE CONFIGURATION


########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
#     }
# }
########## END CACHE CONFIGURATION


########## TOOLBAR CONFIGURATION
# See: https://github.com/django-debug-toolbar/django-debug-toolbar#installation
INSTALLED_APPS += (
    'debug_toolbar',
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

DISQUS_WEBSITE_SHORTNAME = 'cshc-local'

########## END django-disqus CONFIGURATION
