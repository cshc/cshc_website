# Django settings for cshcsite project - common


from os.path import abspath, basename, dirname, join, normpath
from os import environ
from sys import path


# Normally you should not import ANYTHING from Django directly
# into your settings, but ImproperlyConfigured is an exception.
from django.core.exceptions import ImproperlyConfigured


def get_env_setting(setting):
    """ Get the environment setting or return exception """
    try:
        return environ[setting]
    except KeyError:
        error_msg = "Set the %s env variable" % setting
        raise ImproperlyConfigured(error_msg)


########## PATH CONFIGURATION
# Absolute filesystem path to the Django project directory:
DJANGO_ROOT = dirname(dirname(abspath(__file__)))

# Absolute filesystem path to the top-level project folder:
SITE_ROOT = dirname(DJANGO_ROOT)

# Site name:
SITE_NAME = 'CSHC'

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)

VERSION = open(normpath(join(SITE_ROOT, '..', 'version.txt'))).read().lstrip('v').rstrip()

########## END PATH CONFIGURATION


########## DEBUG CONFIGURATION

# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG

TEMPLATE_STRING_IF_INVALID = '######'
########## END DEBUG CONFIGURATION


########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Graham McCulloch', 'website@cambridgesouthhockeyclub.co.uk'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

SERVER_EMAIL = 'website@cambridgesouthhockeyclub.co.uk'

########## END MANAGER CONFIGURATION

########## AUTHENTICATION CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-AUTH_USER_MODEL
AUTH_USER_MODEL = 'core.CshcUser'

########## END AUTHENTICATION CONFIGURATION

########## GENERAL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#time-zone
TIME_ZONE = 'Europe/London'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = 'en-gb'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True

# See: https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

SESSION_COOKIE_AGE = 30*24*60*60   # 30 days in seconds

########## END GENERAL CONFIGURATION


########## MEDIA CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-root
MEDIA_ROOT = normpath(join(SITE_ROOT, 'media'))

# See: https://docs.djangoproject.com/en/dev/ref/settings/#media-url
MEDIA_URL = '/media/'
########## END MEDIA CONFIGURATION


########## STATIC FILE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = normpath(join(SITE_ROOT, 'assets'))
#STATIC_ROOT = 'staticfiles'

# See: https://docs.djangoproject.com/en/dev/ref/settings/#static-url
STATIC_URL = '/static/'

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = (
    normpath(join(SITE_ROOT, 'static')),
)

# See: https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
########## END STATIC FILE CONFIGURATION


########## SECRET CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = get_env_setting('CSHCSITE_SECRET_KEY')
########## END SECRET CONFIGURATION


########## FIXTURE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#std:setting-FIXTURE_DIRS
FIXTURE_DIRS = (
    normpath(join(SITE_ROOT, 'fixtures')),
)
########## END FIXTURE CONFIGURATION


########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-context-processors
TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'django.core.context_processors.request',
    'django_mobile.context_processors.flavour',
    'core.context_processors.utils',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-loaders
TEMPLATE_LOADERS = (
    'django_mobile.loader.Loader',    # Must be the first item apparently
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-dirs
TEMPLATE_DIRS = (
    normpath(join(SITE_ROOT, 'templates')),
)
########## END TEMPLATE CONFIGURATION


########## MIDDLEWARE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#middleware-classes
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django_mobile.middleware.MobileDetectionMiddleware',
    'django_mobile.middleware.SetFlavourMiddleware',
    'pagination.middleware.PaginationMiddleware',
    'maintenancemode.middleware.MaintenanceModeMiddleware',
)
########## END MIDDLEWARE CONFIGURATION


########## URL CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#root-urlconf
ROOT_URLCONF = 'cshcsite.urls'
########## END URL CONFIGURATION


########## APP CONFIGURATION
DJANGO_APPS = (
    # Default Django apps:
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Useful template tags:
    'django.contrib.humanize',
    'django.contrib.sitemaps',

    # Even though we don't use it, the Zinnia admin
    # template requires this app
    'django_comments',

    # Admin panel and documentation:
    'autocomplete_light', # (must come before django.contrib.admin)
    'suit', # http://django-suit.readthedocs.org/en/develop/#installation (must come before django.contrib.admin)
    'django.contrib.admin',
    # 'django.contrib.admindocs',

    'django.contrib.flatpages'  # Potential syncdb error: this may need to be added later in the sequence of installed apps
)

THIRD_PARTY_APPS = (
    # Database migration helpers:
    'south',
    # Mobile support:
    'django_mobile',
    #'easy_thumbnails',
    'captcha',
    'sorl.thumbnail',
    'pagination',
    'sorter',
    'disqus',
    'maintenancemode',
    'storages',
    's3_folder_storage',
    'dbbackup',
    'registration',
    'tagging',
    'mptt',
    'zinnia',
    'redactor',
    'rest_framework',
    'imagekit',
    'geoposition',
)

# Apps specific for this project go here.
LOCAL_APPS = (
    'core',
    'venues',
    'competitions',
    'teams',
    'opposition',
    'members',
    'matches',
    'awards',
    'training',
    'commentary',
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#installed-apps
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
########## END APP CONFIGURATION


########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging
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
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        },
        'file': {
            'level': 'WARN',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': join(SITE_ROOT, '..', '..', 'django.log'),
            'maxBytes': '16777216', # 16megabytes
        },

    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
        # Ignore Invalid HTTP_HOST header messages
        # Ref: http://stackoverflow.com/a/25787817
        'django.security.DisallowedHost': {
            'handlers': ['console'],
            'propagate': False,
        },
        'awards': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
         },
        'competitions': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
         },
        'core': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
         },
        'cshcsite': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
         },
        'matches': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
         },
        'commentary': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
         },
        'members': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
         },
        'opposition': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
         },
        'teams': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
         },
        'training': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
         },
        'venues': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
         },

    }
}
########## END LOGGING CONFIGURATION


########## WSGI CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#wsgi-application
WSGI_APPLICATION = 'wsgi.application'
########## END WSGI CONFIGURATION


########## MODEL-UTILS CONFIGURATION
# See: https://github.com/carljm/django-model-utils
SPLIT_MARKER = '<!-- split -->'
SPLIT_DEFAULT_PARAGRAPHS = 1
########## END MODEL-UTILS CONFIGURATION

########## TWITTER-TAGS CONFIGURATION [NOT USED]
# Not specific to twitter-tags app, but a convenient place to store the default twitter account name
DEFAULT_TWITTER_USER = 'cambsouthhc'

# See: https://github.com/coagulant/django-twitter-tag
# Note: These are currently linked to the Twitter account of cambsouthhc.
# Your access token: Access token
TWITTER_OAUTH_TOKEN = '86176852-vQBOQX4D7nJR1jqLYbXT2fbmf06j7IrCKAZJXCIDM'
# Your access token: Access token secret
TWITTER_OAUTH_SECRET = 'ml7wNoPHVoenJqAKN6nRlQpgxogi3HxGAjVvc1YE'
# OAuth settings: Consumer key
TWITTER_CONSUMER_KEY = 'SZ002z95a6FDnogKmApF7A'
# OAuth settings: Consumer secret
TWITTER_CONSUMER_SECRET = 'UDzGvhx2qQBodi8PY70a6ShFp2j0hZHocr7ZardkdlU'

########## END TWITTER-TAGS CONFIGURATION

########## MISC CONFIGURATION

# See: https://docs.djangoproject.com/en/1.5/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = 'website@cambridgesouthhockeyclub.co.uk'

# See: https://docs.djangoproject.com/en/1.5/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = 'user_profile'
# See https://docs.djangoproject.com/en/1.5/ref/settings/#login-url
LOGIN_URL = 'auth_login'
# See https://docs.djangoproject.com/en/1.5/ref/settings/#logout-url
LOGOUT_URL = 'auth_logout'

########## END MISC CONFIGURATION

########## DJANGO SUIT CONFIGURATION
# See: http://django-suit.readthedocs.org/en/develop/

SUIT_CONFIG = {
    # header
    'ADMIN_NAME': 'Cambridge South Hockey Club - Admin',
    # 'HEADER_DATE_FORMAT': 'l, j. F Y',
    # 'HEADER_TIME_FORMAT': 'H:i',

    # forms
    # 'SHOW_REQUIRED_ASTERISK': True,  # Default True
    # 'CONFIRM_UNSAVED_CHANGES': True, # Default True

    # menu
    # 'SEARCH_URL': '/admin/auth/user/',
    # 'MENU_ICONS': {
    #    'sites': 'icon-leaf',
    #    'auth': 'icon-lock',
    # },
    # 'MENU_OPEN_FIRST_CHILD': True, # Default True
    # 'MENU_EXCLUDE': ('auth.group',),
    # 'MENU': (
    #     'sites',
    #     {'app': 'auth', 'icon':'icon-lock', 'models': ('user', 'group')},
    #     {'label': 'Settings', 'icon':'icon-cog', 'models': ('auth.user', 'auth.group')},
    #     {'label': 'Support', 'icon':'icon-question-sign', 'url': '/support/'},
    # ),

    # misc
    # 'LIST_PER_PAGE': 15
}
########## END DJANGO SUIT CONFIGURATION


########## SORL-THUMBNAIL CONFIGURATION
# See: http://sorl-thumbnail.readthedocs.org/en/latest/reference/settings.html

THUMBNAIL_KVSTORE = 'sorl.thumbnail.kvstores.cached_db_kvstore.KVStore'
#THUMBNAIL_ENGINE = 'sorl.thumbnail.engines.pgmagick_engine.Engine'
THUMBNAIL_DEBUG = True
########## END SORL-THUMBNAIL CONFIGURATION



########## django-sorter CONFIGURATION
SORTER_ALLOWED_CRITERIA = {
    'sort': ['our_team',
             'opp_team',
             'venue',
             'fixture_type',
             'date',
             'home_away',
             'alt_outcome',
             'our_score',
             'opp_score',
             'season',
             'division',
             'cup',
             'first_name',
             'last_name',
             'gender',
             'pref_position',
             'is_current',
             'is_home',
    ],
}
########## END django-sorter CONFIGURATION

########## django-disqus CONFIGURATION

#DISQUS_API_KEY = 'cV5DeRXeXa1NZVvTc00HESt5HNHQEVN5TiQTbqcwEWsOVoawhysgopJ1OfLUcYqH'
DISQUS_API_KEY = 'k5gco5q9gAoR6PmhuODFNOe8If9TgSKkfxHp4owzKMUkLs5rRo2yOjantf17yQiZ'


# Ref: http://disqus.com/api/applications/
DISQUS_SECRET_KEY = 'o1XieDDAFW4YynNcQgSCCjPfeU8mv9YR0GN6i30m1z2yjnwaVpJ2sP2UmxSxu9JO'
DISQUS_PUBLIC_KEY = 'k5gco5q9gAoR6PmhuODFNOe8If9TgSKkfxHp4owzKMUkLs5rRo2yOjantf17yQiZ'

########## END django-disqus CONFIGURATION


########## django-maintenancemode CONFIGURATION
# Ref: https://pypi.python.org/pypi/django-maintenancemode

MAINTENANCE_MODE = False
MAINTENANCE_IGNORE_URLS = (
    r'^/admin/.*',
)
########## END django-maintenancemode CONFIGURATION

########## django-storages CONFIGURATION
# Ref: http://blog.doismellburning.co.uk/2012/07/14/using-amazon-s3-to-host-your-django-static-files/

if not DEBUG:
    AWS_QUERYSTRING_AUTH = False
    AWS_ACCESS_KEY_ID = get_env_setting('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = get_env_setting('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = get_env_setting('AWS_STORAGE_BUCKET_NAME')
    DEFAULT_FILE_STORAGE = 'cshcsite.util.FixedDefaultStorage'
    DEFAULT_S3_PATH = "media"
    STATICFILES_STORAGE = 'cshcsite.util.FixedStaticStorage'
    STATIC_S3_PATH = "static"
    MEDIA_ROOT = '/%s/' % DEFAULT_S3_PATH
    MEDIA_URL = 'https://%s.s3.amazonaws.com/media/' % AWS_STORAGE_BUCKET_NAME
    STATIC_ROOT = "/%s/" % STATIC_S3_PATH
    STATIC_URL = 'https://%s.s3.amazonaws.com/static/' % AWS_STORAGE_BUCKET_NAME
########## END django-storages CONFIGURATION

########## templated-emails CONFIGURATION
# Ref: https://github.com/philippWassibauer/templated-emails
TEMPLATEDEMAILS_USE_PYNLINER = True
#TEMPLATEDEMAILS_USE_CELERY = True
########## END templated-emails CONFIGURATION

########## django-dbbackup CONFIGURATION
# Ref: https://pypi.python.org/pypi/django-dbbackup
DBBACKUP_STORAGE = 'dbbackup.storage.s3_storage'
DBBACKUP_S3_BUCKET = get_env_setting('AWS_STORAGE_BUCKET_NAME')
DBBACKUP_S3_ACCESS_KEY = get_env_setting('AWS_ACCESS_KEY_ID')
DBBACKUP_S3_SECRET_KEY = get_env_setting('AWS_SECRET_ACCESS_KEY')
DBBACKUP_S3_DIRECTORY = 'django-dbbackups/'
########## END django-dbbackup CONFIGURATION

########## django-registration CONFIGURATION
# Ref: https://django-registration.readthedocs.org/en/latest/quickstart.html
ACCOUNT_ACTIVATION_DAYS = 7
########## END django-registration CONFIGURATION

########## django-blog-zinnia CONFIGURATION
# Ref: http://django-blog-zinnia.readthedocs.org/en/v0.14.1/ref/settings.html
# disable comments, pingbacks and trackbacks completely (we'll use disqus)
ZINNIA_AUTO_CLOSE_COMMENTS_AFTER = 0
ZINNIA_AUTO_CLOSE_PINGBACKS_AFTER = 0
ZINNIA_AUTO_CLOSE_TRACKBACKS_AFTER = 0

########## django-redactorjs CONFIGURATION
# Ref: https://github.com/TigorC/django-redactorjs
REDACTOR_OPTIONS = {'lang': 'en',}
REDACTOR_UPLOAD = 'uploads/'
REDACTOR_CSS = {
    'all': (
        STATIC_URL + 'redactor/redactor.css',)
}
REDACTOR_JS = [
    '//ajax.googleapis.com/ajax/libs/jquery/1.11.0/jquery.min.js',
    STATIC_URL + 'redactor/redactor.js',
]

import uuid
def make_unique_filename(filename):
    ext = filename.split('.')[-1]
    return "%s.%s" % (uuid.uuid4(), ext)

REDACTOR_GENERATE_FILENAME = make_unique_filename

########## djangorestframework CONFIGURATION
# Ref: http://www.django-rest-framework.org/tutorial/quickstart#settings
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.AllowAny',),
}
########## END djangorestframework CONFIGURATION


########## django-geoposition CONFIGURATION
# Ref:https://github.com/philippbosch/django-geoposition
GEOPOSITION_GOOGLE_MAPS_API_KEY  = get_env_setting('GOOGLE_MAPS_API_KEY')
GEOPOSITION_MAP_OPTIONS = {
    'minZoom': 3,
    'maxZoom': 15,
    'scrollwheel': True,
    'lat': 52.206133926014665,
    'lng': 0.12531280517578125,
}
########## END django-geoposition CONFIGURATION

# ########## django-recaptcha CONFIGURATION

NOCAPTCHA = True
RECAPTCHA_PUBLIC_KEY = get_env_setting('RECAPTCHA_PUBLIC_KEY')
RECAPTCHA_PRIVATE_KEY = get_env_setting('RECAPTCHA_PRIVATE_KEY')

# ########## END django-recaptcha CONFIGURATION
