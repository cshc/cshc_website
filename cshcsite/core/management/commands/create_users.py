#!/usr/bin/env python
# -*-encoding: utf-8-*-
import sys
import csv
import os
import traceback
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from members.models import Member

USERS_DIR = "import"
USERS_FILE = "users.csv"

class MemberDetails:

    def __init__(self, row):
        self.first_name = row[0]
        self.last_name = row[1]
        self.email = row[2]
    
    
def are_same(member_details, user):
    return (member_details.first_name == user.first_name and  
            member_details.last_name == user.last_name)
            
            
def are_same(member_details, member):  
    return (member_details.first_name == member.first_name and  
            member_details.last_name == member.last_name)
            
            
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
        
        # Get all players
        all_players = Member.objects.all()
        
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
        
        # Get all users
        all_users = User.objects.all()
        
        
        
        