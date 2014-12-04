""" Django settings for cshcsite project - production environment
"""

from cshcsite.settings.base import *

#SESSION_COOKIE_SECURE = True
#CSRF_COOKIE_SECURE = True

ALLOWED_HOSTS = ['www.cambridgesouthhockeyclub.co.uk', 'cambridgesouthhockeyclub.co.uk']

TEMPLATE_STRING_IF_INVALID = ''

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = 'smtp.sendgrid.net'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = get_env_setting('EMAIL_HOST_PASSWORD')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = get_env_setting('EMAIL_HOST_USER')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 587

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = 'website@cambridgesouthhockeyclub.co.uk'
########## END EMAIL CONFIGURATION

########## DATABASE CONFIGURATION
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'cshc',
        'USER': 'cshc',
        'PASSWORD': get_env_setting('DB_PASSWORD'),
        'HOST': 'mysql-51.int.mythic-beasts.com',
        'PORT': '',
    }
}
########## END DATABASE CONFIGURATION

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
#CACHES = {}
########## END CACHE CONFIGURATION

########## django-disqus CONFIGURATION

DISQUS_WEBSITE_SHORTNAME = 'cshc-prod'

########## END django-disqus CONFIGURATION
