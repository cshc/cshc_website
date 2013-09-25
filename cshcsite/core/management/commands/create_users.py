#!/usr/bin/env python
# -*-encoding: utf-8-*-
import csv
import os
import collections
import traceback
from optparse import make_option
from django.core.management.base import BaseCommand
from django.conf import settings
from core.models import CshcUser, is_none_or_empty
from members.models import Member

USERS_DIR = "import"
USERS_FILE = "users.csv"

EMAIL_COL = 0
EMIAL_OPT_COL = 1
FIRST_NAME_COL = 3
LAST_NAME_COL = 4
SHIR_NUMBER_COL = 20


class MemberDetails:

    def __init__(self, row):
        self.receive_emails = True if bytearray(row[EMIAL_OPT_COL]).decode('utf-8') == 'Receive all e-mails' else False
        self.first_name = bytearray(row[FIRST_NAME_COL]).decode('utf-8')
        self.last_name = bytearray(row[LAST_NAME_COL]).decode('utf-8')
        self.email = bytearray(row[EMAIL_COL]).decode('utf-8')
        self.shirt_number = bytearray(row[SHIR_NUMBER_COL]).decode('utf-8').lstrip('[').rstrip(']')
        if is_none_or_empty(self.shirt_number):
            self.shirt_number = None

    def __hash__(self):
        return hash(self.first_name) ^ hash(self.last_name)

    def __eq__(self, other):
        return isinstance(other, self.__class__) and details_same(self, other)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return "{} {} - {}".format(self.first_name, self.last_name, self.email)


def details_same_as_user(member_details, user):
    return (member_details.first_name == user.first_name and
            member_details.last_name == user.last_name)


def details_same_as_member(member_details, member):
    return (member_details.first_name == member.first_name and
            member_details.last_name == member.last_name)


def details_same(a, b):
    return (a.first_name == b.first_name and
            a.last_name == b.last_name)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--sim',
                    action='store_true',
                    dest='simulate',
                    default=False,
                    help='Test run (doesn\'t actually create the users)'),
    )
    help = 'Automatically creates users for all players, if found in the csv file'

    def handle(self, *args, **options):
        try:
            self._handle(*args, **options)
        except:
            traceback.print_exc()

    def _handle(self, *args, **options):

        # Get all players without an associated user
        userless_players = Member.objects.all().filter(user__isnull=True)

        # Read in all members from the csv file
        members = []
        filename = os.path.join(settings.SITE_ROOT, USERS_DIR, USERS_FILE)
        with open(filename, 'rb') as f:
            reader = csv.reader(f)
            first_row = True
            for csv_row in reader:
                # Ignore the first row (field names)
                if first_row:
                    first_row = False
                    continue
                m = MemberDetails(csv_row)
                if m.receive_emails:
                    members.append(m)

        print "============================"
        print "Read {} member details from CSV file".format(len(members))
        # Find duplicates
        duplicates = [x for x, y in collections.Counter(members).items() if y > 1]
        print "============================"
        print "Found {} duplicates:".format(len(duplicates))
        for d in duplicates:
            print d

        print "============================"
        print "Removing duplicates"
        members = set(members)
        print "{} unique member details".format(len(members))

        conversion_count = 0
        for player in userless_players:
            try:
                matching_details = next(x for x in members if details_same_as_member(x, player))
            except StopIteration:
                # Players without a user associated with them are deemed not to be current
                player.is_current = False
                player.save()
            else:
                u = self.create_user(matching_details, options['simulate'], player)
                player.user = u
                # Players with a user associated with them are deemed to be current
                player.is_current = True
                player.save()
                print "Associating User '{}' with Member '{}'".format(u, player)
                members.remove(matching_details)
                conversion_count += 1

        print "DONE: Associated {} Users with Members".format(conversion_count)


    def create_user(self, member_details, simulate, player):
        try:
            new_user = CshcUser.objects.get(email=member_details.email)
        except CshcUser.DoesNotExist:
            if not simulate:
                new_user = CshcUser.objects.create_user(email=member_details.email,
                                                        first_name=member_details.first_name,
                                                        last_name=member_details.last_name)
            else:
                new_user = CshcUser(email=member_details.email,
                                    first_name=member_details.first_name,
                                    last_name=member_details.last_name)
        else:
            print "WARNING: User already exists with email '{}'".format(member_details.email)
        if not player.shirt_number and member_details.shirt_number:
            player.shirt_number = member_details.shirt_number
            if not simulate:
                player.save()
            print "{} shirt number = {}".format(player.full_name(), player.shirt_number)
        return new_user
