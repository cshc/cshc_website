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
SITE_NAME = basename(DJANGO_ROOT)

# Add our project to our pythonpath, this way we don't need to type our project
# name in our dotted import paths:
path.append(DJANGO_ROOT)
########## END PATH CONFIGURATION


########## DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = False

# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug
TEMPLATE_DEBUG = DEBUG
########## END DEBUG CONFIGURATION


########## MANAGER CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = (
    ('Graham McCulloch', 'admin@grahammcculloch.co.uk'),
)

# See: https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS
########## END MANAGER CONFIGURATION


########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.',
        'NAME': '',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}
########## END DATABASE CONFIGURATION


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
# Note: This key only used for development and testing.
SECRET_KEY = r"{{ secret_key }}"
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
ROOT_URLCONF = '%s.urls' % SITE_NAME
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

    # Admin panel and documentation:
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
    'tinymce',
    #'easy_thumbnails',
    'sorl.thumbnail',
    'pagination',
    'sorter',
    'disqus',
    'maintenancemode',
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
        # 'file': {
        #     'level': 'WARN',
        #     'class': 'logging.FileHandler',
        #     'filename': '../../logs/debug.log',
        # },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'awards': {
            'handlers': ['console'],
            'level': 'DEBUG',
         },
        'competitions': {
            'handlers': ['console'],
            'level': 'DEBUG',
         },
        'core': {
            'handlers': ['console'],
            'level': 'DEBUG',
         },
        'cshcsite': {
            'handlers': ['console'],
            'level': 'DEBUG',
         },
        'matches': {
            'handlers': ['console'],
            'level': 'DEBUG',
         },
        'members': {
            'handlers': ['console'],
            'level': 'DEBUG',
         },
        'mobile': {
            'handlers': ['console'],
            'level': 'DEBUG',
         },
        'opposition': {
            'handlers': ['console'],
            'level': 'DEBUG',
         },
        'teams': {
            'handlers': ['console'],
            'level': 'DEBUG',
         },
        'training': {
            'handlers': ['console'],
            'level': 'DEBUG',
         },
        'venues': {
            'handlers': ['console'],
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
DEFAULT_FROM_EMAIL = 'webmaster@cambridgesouthhockeyclub.co.uk'

# See: https://docs.djangoproject.com/en/1.5/ref/settings/#login-redirect-url
LOGIN_REDIRECT_URL = 'user_profile'
# See https://docs.djangoproject.com/en/1.5/ref/settings/#login-url
LOGIN_URL = 'login'
# See https://docs.djangoproject.com/en/1.5/ref/settings/#logout-url
LOGOUT_URL = 'logout'

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

########## TINYMCE CONFIGURATION
# See: http://django-tinymce.readthedocs.org/en/latest/

TINYMCE_DEFAULT_CONFIG = {
    'plugins': 'table,spellchecker,paste,searchreplace,preview',
    'theme': 'advanced',
    'theme_advanced_buttons3_add': 'preview',
    'plugin_preview_width': '900',
    'plugin_preview_height': '800',
    'content_css':'/static/css/project_preview.css',
}
########## END TINYMCE CONFIGURATION

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

DISQUS_API_KEY = 'cV5DeRXeXa1NZVvTc00HESt5HNHQEVN5TiQTbqcwEWsOVoawhysgopJ1OfLUcYqH'


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
