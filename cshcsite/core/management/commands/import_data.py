import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cshcsite.settings.local")

import sys
import csv
import traceback
from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option
from datetime import date
from teams.models import TeamCaptaincy

IMPORT_DIR = 'import'

DATE_FORMAT = '%d/%m/%Y'    # e.g. '01/09/2009'

class TeamCaptainCsv:

    def __init__(self, row):
        self.team = bytearray(row[0]).decode('utf-8')
        self.name = bytearray(row[1]).decode('utf-8')
        self.is_vice = bytearray(row[2]).decode('utf-8') == 'y'
        self.start = date.strptime(bytearray(row[3]).decode('utf-8'), DATE_FORMAT)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--sim',
                    action='store_true',
                    dest='simulate',
                    default=False,
                    help='Test run (doesn\'t actually save any imported data)'),
        make_option('-f', '--file',
                    action='store',
                    type="string",
                    dest='filename',
                    metavar='FILE',
                    help='Import data from FILE'),
        )
    help = 'Import data from csv files'

    def handle(self, *args, **options):
        try:
            self._handle(*args, **options)
        except:
            traceback.print_exc()

    def _handle(self, *args, **options):
        filename = options['filename']
        sim = options['simulate']
        if filename == 'team_captains.csv':
            Command.import_team_captains(filename, sim)

    @staticmethod
    def import_team_captains(filename, sim):
        file_path = os.path.join(settings.SITE_ROOT, IMPORT_DIR, filename)
        captains = []
        with open(file_path, 'rb') as source_file:
            reader = csv.reader(source_file)
            first_row = True
            for csv_row in reader:
                # Ignore the first row (field names)
                if first_row:
                    first_row = False
                    continue
                captain = TeamCaptainCsv(csv_row)
                captains.append(captain)

        for captain in captains:
            # Try to find matching captain in TeamCaptaincy
            try:
                captaincy = TeamCaptaincy.objects.where()
            except TeamCaptaincy.DoesNotExist:
                pass
