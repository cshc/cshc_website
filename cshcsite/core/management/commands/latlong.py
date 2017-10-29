"""
Temporary management command used to import latitidue/longitude positions for all venues.

The command takes one argument - the filename of a CSV file with the venue positions listed.

The CSV file should not contain a header row and each row must have three columns:
  0: venue ID
  1: latitude
  2: longitude

"""
import csv
import os.path
import traceback
from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from venues.models import Venue


class Command(BaseCommand):

    def __init__(self):
        super(Command, self).__init__()

    def handle(self, *args, **options):
        file_path = args[0]
        if not os.path.isfile(file_path):
            print("ERROR: No such file {}".format(file_path))
            return

        with open(file_path, 'rb') as source_file:
            reader = csv.reader(source_file)
            try:
                while True:
                    csv_row = reader.next()
                    venueId = csv_row[0]
                    position = "{},{}".format(csv_row[1], csv_row[2])
                    try:
                      v = Venue.objects.get(id=venueId)
                      v.position = position
                      v.save()
                      print("Saved {} ({})".format(v.name, position))
                    except ObjectDoesNotExist:
                      print("Could not find venue with ID = {}".format(venueId))
            except StopIteration:
                pass    # We're done!
            except:
                traceback.print_exc()
