# Django settings for cshcsite project - staging environment (Heroku)
from .base import *
import dj_database_url


MAINTENANCE_MODE = True

DEBUG = True
TEMPLATE_DEBUG = DEBUG

TEMPLATE_STRING_IF_INVALID = '######'

########## DATABASE CONFIGURATION
DATABASES = {'default': dj_database_url.config()}
########## END DATABASE CONFIGURATION

ALLOWED_HOSTS = ['*']

########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = get_env_setting('CSHCSITE_SECRET_KEY')
########## END SECRET CONFIGURATION

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

########## django-disqus CONFIGURATION

DISQUS_WEBSITE_SHORTNAME = 'cshc-staging'

########## END django-disqus CONFIGURATION


########## EMAIL CONFIGURATION
EMAIL_HOST = 'smtp.sendgrid.net'
EMAIL_HOST_USER = get_env_setting('SENDGRID_USERNAME')
EMAIL_HOST_PASSWORD = get_env_setting('SENDGRID_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True
########## END EMAIL CONFIGURATION



