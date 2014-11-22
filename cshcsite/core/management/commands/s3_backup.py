import boto
import gzip
from django.core.management.base import BaseCommand
from django.core.mail import send_mail

PROD_BUCKET_NAME = 'cshc'
STAGING_BUCKET_NAME = 'cshc-c9'
BACKUPS_KEY_PREFIX = 'django-dbbackups'
BACKUP_FILENAME = '~/prod_dump.mysql'
GZ_BACKUP_FILENAME = BACKUP_FILENAME + '.gz'

class Command(BaseCommand):
    def handle(self, *args, **options):

        errors = []
        try:
            conn = boto.connect_s3()
            prod_bucket = conn.get_bucket(PROD_BUCKET_NAME)
            c9_bucket = conn.get_bucket(STAGING_BUCKET_NAME)

            # 1. Download and unzip the latest MySQL database backup from its S3 storage location
            backups = list(prod_bucket.list(prefix=BACKUPS_KEY_PREFIX))
            latest_backup = sorted(backups, key=lambda b: b.last_modified, reverse=True)[0]

            latest_backup.get_contents_to_filename(GZ_BACKUP_FILENAME)

            with gzip.open(GZ_BACKUP_FILENAME, 'rb') as inF:
                with open(BACKUP_FILENAME, 'wb') as outF:
                    outF.write( inF.read() )

            # 2. Copy all keys from production bucket's media/ directory to the corresponding
            #    staging bucket's media/ directory
            for media_key in prod_bucket.list(prefix='media'):
                c9_bucket.copy_key(media_key.name, PROD_BUCKET_NAME, media_key.name)

        except Exception as e:
            errors.add("S3 (boto) error: {}".format(e))

        if errors:
            send_mail("Automated S3 backup task failed", "\n".join(errors), 'website@cambridgesouthhockeyclub.co.uk', ['website@cambridgesouthhockeyclub.co.uk'])
