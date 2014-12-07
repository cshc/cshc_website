""" Management command that does the following:

    1) Downloads the latest database backup from Amazon S3 and
       saves it to BACKUP_FILENAME
    2) Copies each key (file) from the production Amazon S3 bucket
       to the staging/testing Amazon S3 bucket.

    This command is used as part of a series of actions to update the
    staging site with data from the production site. See shell scripts
    on the Cloud9 VM for more details.

    Usage:
    python manage.py s3_backup

"""

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

            with gzip.open(GZ_BACKUP_FILENAME, 'rb') as in_file:
                with open(BACKUP_FILENAME, 'wb') as out_file:
                    out_file.write(in_file.read())

            # 2. Copy all keys from production bucket's media/ directory to the corresponding
            #    staging bucket's media/ directory
            for media_key in prod_bucket.list(prefix='media'):
                c9_bucket.copy_key(media_key.name, PROD_BUCKET_NAME, media_key.name, preserve_acl=True)

        except Exception as e:
            errors.append("S3 (boto) error: {}".format(e))

        if errors:
            send_mail("Automated S3 backup task failed", "\n".join(errors),
                      'website@cambridgesouthhockeyclub.co.uk',
                      ['website@cambridgesouthhockeyclub.co.uk'])
