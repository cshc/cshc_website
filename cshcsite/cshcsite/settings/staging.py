# Django settings for cshcsite project - staging environment (Heroku)
from .base import *
import dj_database_url

DEBUG = False
TEMPLATE_DEBUG = DEBUG

TEMPLATE_STRING_IF_INVALID = '######'

########## DATABASE CONFIGURATION
DATABASES = {'default': dj_database_url.config()}
########## END DATABASE CONFIGURATION

ALLOWED_HOSTS = ['*']

# Ref: https://pypi.python.org/pypi/dj-static
#STATIC_ROOT = 'staticfiles'
STATIC_ROOT = normpath(join(SITE_ROOT, 'assets'))

########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = get_env_setting('CSHCSITE_SECRET_KEY')
########## END SECRET CONFIGURATION

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

########## django-disqus CONFIGURATION

DISQUS_WEBSITE_SHORTNAME = 'cshc-staging'

########## END django-disqus CONFIGURATION
