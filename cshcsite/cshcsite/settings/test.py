# Django settings for cshcsite project - test environment
from .base import *

########## TEST SETTINGS
TEST_RUNNER = 'discover_runner.DiscoverRunner'
TEST_DISCOVER_TOP_LEVEL = SITE_ROOT
TEST_DISCOVER_ROOT = SITE_ROOT
TEST_DISCOVER_PATTERN = "test_*.py"

########## IN-MEMORY TEST DATABASE
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
        "USER": "",
        "PASSWORD": "",
        "HOST": "",
        "PORT": "",
    },
}

########## django-disqus CONFIGURATION

DISQUS_WEBSITE_SHORTNAME = 'cshc-test'

########## END django-disqus CONFIGURATION
