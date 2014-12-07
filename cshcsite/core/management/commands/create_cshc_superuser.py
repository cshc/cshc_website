""" Management command to create a CSHC superuser.

    Usage:
    python manage.py create_cshc_superuser

    Note: the following environment variables need to be set first:
    SUPERUSER_EMAIL
    SUPERUSER_PASSWORD
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from cshcsite.settings.base import get_env_setting


class Command(BaseCommand):
    """ Management command to create a CSHC superuser. """

    def handle(self, *args, **options):
        get_user_model().objects.create_superuser(email=get_env_setting('SUPERUSER_EMAIL'),
                                                  password=get_env_setting('SUPERUSER_PASSWORD'))
