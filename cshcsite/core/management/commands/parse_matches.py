import os
import sys
import csv
import inspect
from django.core.management.base import BaseCommand, CommandError
from django.core.exceptions import ObjectDoesNotExist
from _old_data_structures import *

IMPORT_DIR = 'import'
MDB_FILE = 'CSHC_2009.mdb'
CONVERSION_OUTPUT_DIR = 'csv'


class OldTable:

    def __init__(self, table_name, table_class):
        self.table_name = table_name
        self.table_class = table_class
        self.rows = {}


def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except ObjectDoesNotExist:
        return None

class Command(BaseCommand):

    def handle(self, *args, **options):
        #######################################################################
        # SETUP PARSING

        # Get a list of table classes
        old_data_table_classes = inspect.getmembers(sys.modules['core.management.commands._old_data_structures'], inspect.isclass)
        # Dictionary to store table names and corresponding classes
        old_tables = {}

        for table in old_data_table_classes:
            if table[0] == 'Old_Table_Entry':
                continue
            table_name = table[0][4:]
            table_class = table[1]
            old_table = OldTable(table_name, table_class)
            if table_name in args:
                old_tables[table_name] = old_table

        #######################################################################
        # PARSE CSV FILES

        file_path = os.path.join('.', IMPORT_DIR, CONVERSION_OUTPUT_DIR, '{0}.TXT'.format('Matches_manual'))
        with open(file_path, 'rb') as table_file:
            reader = csv.reader(table_file)
            first = True
            for csv_row in reader:
                if csv_row[0] == old_tables['Matches'].table_class.field_names[0]:
                    continue

                field_values = csv_row
                row = old_tables['Matches'].table_class(field_values)
                old_table.rows[row.pk] = row

            print "Imported {0} rows from {1}".format(len(old_table.rows), old_tables['Matches'].table_name)