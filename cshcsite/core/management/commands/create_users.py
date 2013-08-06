#!/usr/bin/env python
# -*-encoding: utf-8-*-
import csv
import os
import collections
import traceback
from optparse import make_option
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from members.models import Member

USERS_DIR = "import"
USERS_FILE = "users.csv"

EMAIL_COL = 0
FIRST_NAME_COL = 3
LAST_NAME_COL = 4


class MemberDetails:

    def __init__(self, row):
        self.first_name = bytearray(row[FIRST_NAME_COL]).decode('utf-8')
        self.last_name = bytearray(row[LAST_NAME_COL]).decode('utf-8')
        self.email = bytearray(row[EMAIL_COL]).decode('utf-8')

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
        make_option('--test',
                    action='store_true',
                    dest='test',
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
        filename = os.path.join('.', USERS_DIR, USERS_FILE)
        with open(filename, 'rb') as f:
            reader = csv.reader(f)
            first_row = True
            for csv_row in reader:
                # Ignore the first row (field names)
                if first_row:
                    first_row = False
                    continue
                members.append(MemberDetails(csv_row))

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
                pass
            else:
                u = self.create_user(matching_details)
                player.user = u
                player.save()
                print "Associating new User '{}' with Member '{}'".format(u, player)
                members.remove(matching_details)
                conversion_count += 1

        print "DONE: Associated {} Users with Members".format(conversion_count)

    def create_user(self, member_details):
        for i in range(10):
            username = "{}_{}{}".format(member_details.first_name, member_details.last_name, "" if i == 0 else i)
            try:
                new_user = User.objects.create_user(username)
            except:
                print ("WARNING: User already exists with username '{}'".format(username))
                continue
            new_user.first_name = member_details.first_name
            new_user.last_name = member_details.last_name
            new_user.email = member_details.email
            new_user.save()
            return new_user
