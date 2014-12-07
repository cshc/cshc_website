""" Utility code for the CSHC website.
"""

# Fix for S3 path being incorrect:
# Ref: http://code.larlet.fr/django-storages/issue/121/s3boto-admin-prefix-issue-with-django-14
# Github issue #42
from s3_folder_storage.s3 import StaticStorage, DefaultStorage

class FixedStaticStorage(StaticStorage):

    def url(self, name):
        url = super(FixedStaticStorage, self).url(name)
        if name.endswith('/') and not url.endswith('/'):
            url += '/'
        return url

class FixedDefaultStorage(DefaultStorage):

    def url(self, name):
        url = super(FixedDefaultStorage, self).url(name)
        if name.endswith('/') and not url.endswith('/'):
            url += '/'
        return url
