# Django settings for cshcsite project - production environment
from base import *


ALLOWED_HOSTS = ['cambridgesouthhockeyclub.co.uk']

MAINTENANCE_MODE = False

########## EMAIL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
EMAIL_HOST = 'smtp-auth.mythic-beasts.com'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
EMAIL_HOST_PASSWORD = get_env_setting('EMAIL_HOST_PASSWORD')

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', 'webmaster@cambridgesouthhockeyclub.co.uk')    # Important: NOT website@...

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
EMAIL_PORT = 465

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

# See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
EMAIL_USE_TLS = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = EMAIL_HOST_USER
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


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = get_env_setting('CSHCSITE_SECRET_KEY')
########## END SECRET CONFIGURATION

########## django-disqus CONFIGURATION

DISQUS_WEBSITE_SHORTNAME = 'cshc-prod'

########## END django-disqus CONFIGURATION
