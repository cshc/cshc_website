from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from cshcsite.settings.base import get_env_setting

class Command(BaseCommand):
    def handle(self, *args, **options):
        get_user_model().objects.create_superuser(email=get_env_setting('SUPERUSER_EMAIL'), password=get_env_setting('SUPERUSER_PASSWORD'))