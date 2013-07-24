#!/usr/bin/env python
# -*-encoding: utf-8-*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cshcsite.settings.local")

import sys
import csv
import traceback
import subprocess
import re
import inspect
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from optparse import make_option
from core.models import TeamOrdinal
from competitions.models import Cup, Division, League, Season
from members.models import Member
from venues.models import Venue
from teams.models import ClubTeam, ClubTeamSeasonParticipation
from matches.models import Match, Appearance
from awards.models import MatchAward, MatchAwardWinner
from _old_data_structures import *

IMPORT_DIR = 'import'
MDB_FILE = 'CSHC_2009.mdb'
CONVERSION_OUTPUT_DIR = 'csv'

class OldTable:

    def __init__(self, table_name, table_class):
        self.table_name = table_name
        self.table_class = table_class
        self.rows = {}

class NewTableRow:

    def __init__(self, model):
        self.model = model
        self.errors = []


def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--delete',
            action='store_true',
            dest='delete',
            default=False,
            help='Delete existing models'),
        )
    args = '<table_name table_name ...>'
    help = 'Migrates tables from the old MDB file. Use -c to also convert the MDB file to CSV first.'

    def handle(self, *args, **options):
        try:
            self._handle(*args, **options)
        except:
            traceback.print_exc()

    def _handle(self, *args, **options):

        if options['delete']:
            Appearance.objects.all().delete()
            MatchAward.objects.all().delete()
            Match.objects.all().delete()
            ClubTeamSeasonParticipation.objects.all().delete()
            Member.objects.all().delete()
            Team.objects.all().delete()
            Club.objects.all().delete()
            ClubTeam.objects.all().delete()
            Season.objects.all().delete()
            Venue.objects.all().delete()
            Division.objects.all().delete()
            Cup.objects.all().delete()
            League.objects.all().delete()
            return


        #######################################################################
        # SETUP PARSING

        table_list = args if args else [
               'Venues',
               'Teams',
               'Opposition_Clubs',
               'Opposition_Club_Teams',
               'Players',
               'Team_Seasons',
               'Matches',
               'Match_Players'
               ]

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
            if table_name in table_list or table_name == 'Seasons':
                old_tables[table_name] = old_table

        #######################################################################
        # PARSE CSV FILES

        for table_name, old_table in old_tables.iteritems():
            file_path = os.path.join('.', IMPORT_DIR, CONVERSION_OUTPUT_DIR, '{0}.csv'.format(table_name))
            with open(file_path, 'rb') as table_file:
                reader = csv.reader(table_file)
                first_row = True
                for csv_row in reader:
                    # Ignore the first row (field names)
                    if first_row:
                        first_row = False
                        continue
                    row = old_table.table_class(csv_row)
                    old_table.rows[row.pk] = row

                print "Imported {0} rows from {1}".format(len(old_table.rows), table_name)

        #######################################################################
        # FIXUP OLD DATA

        for table_name, old_table in old_tables.iteritems():
            print "Fixing up {0}...".format(table_name)
            for row in old_table.rows.itervalues():
                row.fixup()
            error_count = sum((len(row.errors) for row in old_table.rows.values()))
            if error_count > 0:
                print "Found {0} errors in {1}:".format(error_count, table_name)
            else:
                print "Done."

        #######################################################################
        # VALIDATE OLD DATA

        for table_name, old_table in old_tables.iteritems():
            print "Validating {0}...".format(table_name)
            for row in old_table.rows.itervalues():
                row.validate()
            error_count = sum((len(row.errors) for row in old_table.rows.values()))
            if error_count > 0:
                print "Found {0} errors in {1}".format(error_count, table_name)
            else:
                print "Done."

        #######################################################################
        # Need to do Seasons first

        pre_req = {}
        new_tables = {}
        Command.convert_table('Seasons', old_tables, new_tables, pre_req)

        #######################################################################
        # PRE-REQUISITES
        # These are easier just to check exist first!

        pre_req['ClubTeam'] = Command.add_club_team_prerequisites()
        pre_req['League'] = Command.add_league_prerequisites()
        pre_req['Division'] = Command.add_division_prerequisites(pre_req['League'])
        pre_req['Cup'] = Command.add_cup_prerequisites(pre_req['League'])
        Command.add_clubteamseasonparticipation_prerequisites(pre_req['ClubTeam'], pre_req['Division'], pre_req['Cup'])
        Command.add_matchaward_prerequisites()

        #######################################################################
        # CREATE NEW DATA

        for arg in table_list:
            Command.convert_table(arg, old_tables, new_tables, pre_req)

        #######################################################################
        # PRINT ERRORS

        print ""
        print "ERRORS and WARNINGS =========================================="
        for arg in table_list:
            table_name = arg
            old_table = old_tables[table_name]
            print ""
            print "{0}:".format(table_name)
            for old_id, row in old_table.rows.iteritems():
                for warning in row.warnings:
                    print "WARNING: {0}[{1}] {2}".format(table_name, old_id, warning)
                for error in row.errors:
                    print "ERROR:   {0}[{1}] {2}".format(table_name, old_id, error)


    @staticmethod
    def convert_table(arg, old_tables, new_tables, pre_req):
        table_name = arg
        old_table = old_tables[table_name]

        new_table_name = old_table.table_class.new_table_name
        print "Converting {0} to {1}...".format(table_name, new_table_name)
        new_tables[new_table_name] = {}   # Key = old id, Value = NewTableRow
        invalid_count = 0
        saved_count = 0
        skipped_count = 0

        for old_row in old_table.rows.itervalues():
            if old_row.is_valid:
                new_row = old_row.convert(new_tables, pre_req)
                if new_row:
                    existing_row = get_or_none(old_row.new_table_class, **old_row.existing_check(new_row))
                    try:
                        if not existing_row:
                            new_row.save()
                            print "\tSaved new {0}: [{1}] -> {2}".format(new_table_name, old_row.pk, new_row)
                            saved_count += 1
                        else:
                            print "\tSkipped existing {0}: [{1}] -> {2}".format(new_table_name, old_row.pk, new_row)
                            new_row = existing_row
                            skipped_count += 1
                        new_tables[new_table_name][old_row.pk] = NewTableRow(new_row)
                    except:
                        print "\tFailed to save new {0}: [{1}] -> [{2}]".format(new_table_name, old_row.pk, new_row.pk)
                        traceback.print_exc()
                        invalid_count += 1
                        return
                else:
                    print "\tCould not convert {0}: pk={1}".format(table_name, old_row.pk)
                    invalid_count += 1
            else:
                print "\tSkipping invalid {0}: pk={1}".format(table_name, old_row.pk)
                invalid_count += 1

        print "Done (saved {0}, skipped {1}, invalid {2})".format(saved_count, skipped_count, invalid_count)

    @staticmethod
    def add_club_team_prerequisites():
        new_teams = {}

        new_teams['M1'], created = ClubTeam.objects.get_or_create(short_name='M1', long_name="Men's 1st XI", gender=TeamGender.Mens, ordinal=TeamOrdinal.T1, position=1)
        new_teams['M2'], created = ClubTeam.objects.get_or_create(short_name='M2', long_name="Men's 2nd XI", gender=TeamGender.Mens, ordinal=TeamOrdinal.T2, position=2)
        new_teams['M3'], created = ClubTeam.objects.get_or_create(short_name='M3', long_name="Men's 3rd XI", gender=TeamGender.Mens, ordinal=TeamOrdinal.T3, position=3)
        new_teams['M4'], created = ClubTeam.objects.get_or_create(short_name='M4', long_name="Men's 4th XI", gender=TeamGender.Mens, ordinal=TeamOrdinal.T4, position=4)
        new_teams['M5'], created = ClubTeam.objects.get_or_create(short_name='M5', long_name="Men's 5th XI", gender=TeamGender.Mens, ordinal=TeamOrdinal.T5, position=5)
        new_teams['L1'], created = ClubTeam.objects.get_or_create(short_name='L1', long_name="Ladies' 1st XI", gender=TeamGender.Ladies, ordinal=TeamOrdinal.T1, position=6)
        new_teams['L2'], created = ClubTeam.objects.get_or_create(short_name='L2', long_name="Ladies' 2nd XI", gender=TeamGender.Ladies, ordinal=TeamOrdinal.T2, position=7)
        new_teams['Mixed'], created = ClubTeam.objects.get_or_create(short_name='Mixed', long_name="Mixed XI", gender=TeamGender.Mixed, ordinal=TeamOrdinal.TOther, position=8)
        new_teams['Indoor'], created = ClubTeam.objects.get_or_create(short_name='Indoor', long_name="Indoor Team", gender=TeamGender.Mixed, ordinal=TeamOrdinal.TIndoor, position=9)
        new_teams['Vets'], created = ClubTeam.objects.get_or_create(short_name='Vets', long_name="Vets XI", gender=TeamGender.Mens, ordinal=TeamOrdinal.TVets, position=10)

        return new_teams

    @staticmethod
    def add_cup_prerequisites(leagues):
        new_cups = {}

        new_cups['EHL Vase'], created = Cup.objects.get_or_create(name='EHL Vase', gender=TeamGender.Mens, league=leagues['East League'])
        new_cups['Cambs League Premier Division Cup'], created = Cup.objects.get_or_create(name='Cambs League Premier Division Cup', gender=TeamGender.Ladies, league=leagues['Cambs League'])
        new_cups['Cambs League 1st Division Cup'], created = Cup.objects.get_or_create(name='Cambs League 1st Division Cup', gender=TeamGender.Ladies, league=leagues['Cambs League'])
        new_cups['Cambs League 2nd Division Cup'], created = Cup.objects.get_or_create(name='Cambs League 2nd Division Cup', gender=TeamGender.Ladies, league=leagues['Cambs League'])

        # TEMP!
        new_cups['Indoor Cup'], created = Cup.objects.get_or_create(name='Indoor Cup', gender=TeamGender.Mixed)

        return new_cups

    @staticmethod
    def add_league_prerequisites():
        new_leagues = {}

        new_leagues['East League'], created = League.objects.get_or_create(name='East League')
        new_leagues['Cambs League'], created = League.objects.get_or_create(name='Cambs League')

        return new_leagues

    @staticmethod
    def add_division_prerequisites(leagues):
        new_divisions = {}

        # East Leagues
        new_divisions['Division 3NW'], created = Division.objects.get_or_create(name='Division 3NW', league=leagues['East League'], gender=TeamGender.Mens)
        new_divisions['Division 4NW'], created = Division.objects.get_or_create(name='Division 4NW', league=leagues['East League'], gender=TeamGender.Mens)
        new_divisions['Division 5NW'], created = Division.objects.get_or_create(name='Division 5NW', league=leagues['East League'], gender=TeamGender.Mens)
        new_divisions['Division 6NW(S)'], created = Division.objects.get_or_create(name='Division 6NW(S)', league=leagues['East League'], gender=TeamGender.Mens)
        new_divisions['Division 6NW'], created = Division.objects.get_or_create(name='Division 6NW', league=leagues['East League'], gender=TeamGender.Mens)
        new_divisions['Division 7NW'], created = Division.objects.get_or_create(name='Division 7NW', league=leagues['East League'], gender=TeamGender.Mens)

        # Cambs League
        new_divisions['Premier Division'], created = Division.objects.get_or_create(name='Premier Division', league=leagues['Cambs League'], gender=TeamGender.Ladies)
        new_divisions['1st Division'], created = Division.objects.get_or_create(name='1st Division', league=leagues['Cambs League'], gender=TeamGender.Ladies)
        new_divisions['2nd Division'], created = Division.objects.get_or_create(name='2nd Division', league=leagues['Cambs League'], gender=TeamGender.Ladies)

        return new_divisions

    @staticmethod
    def add_clubteamseasonparticipation_prerequisites(clubteams, divisions, cups):

        # Index of old league tables:
        # http://www.east-leagues.co.uk/leagues/history/oldtables.htm
        # Format for men's leagues for season 20XX-20YY, Division <div>:
        # http://www.east-leagues.co.uk/showdata/EML%20tables%20XXYY.asp?division=<div>
        # TEMP HACK - these are missing from the Team_Seasons table. Github issue #12
        ClubTeamSeasonParticipation.objects.get_or_create(team=clubteams['M1'], season=Season.objects.by_date('2003-12-01'), division=divisions['Division 3NW'],
                                                         division_tables_url='http://www.east-leagues.co.uk/showdata/EML%20tables%200304.asp?division=3NW')
        ClubTeamSeasonParticipation.objects.get_or_create(team=clubteams['M1'], season=Season.objects.by_date('2004-12-01'), division=divisions['Division 3NW'],
                                                         division_tables_url='http://www.east-leagues.co.uk/showdata/EML%20tables%200405.asp?division=3NW')
        ClubTeamSeasonParticipation.objects.get_or_create(team=clubteams['M1'], season=Season.objects.by_date('2005-12-01'), division=divisions['Division 3NW'],
                                                         division_tables_url='http://www.east-leagues.co.uk/showdata/EML%20tables%200506.asp?division=3NW')
        ClubTeamSeasonParticipation.objects.get_or_create(team=clubteams['M1'], season=Season.objects.by_date('2006-12-01'), division=divisions['Division 3NW'],
                                                         division_tables_url='http://www.east-leagues.co.uk/showdata/EML%20tables%200607.asp?division=3NW')

        ClubTeamSeasonParticipation.objects.get_or_create(team=clubteams['M2'], season=Season.objects.by_date('2003-12-01'), division=divisions['Division 5NW'],
                                                         division_tables_url='http://www.east-leagues.co.uk/showdata/EML%20tables%200304.asp?division=5NW')
        ClubTeamSeasonParticipation.objects.get_or_create(team=clubteams['M2'], season=Season.objects.by_date('2004-12-01'), division=divisions['Division 5NW'],
                                                         division_tables_url='http://www.east-leagues.co.uk/showdata/EML%20tables%200405.asp?division=5NW')
        ClubTeamSeasonParticipation.objects.get_or_create(team=clubteams['M2'], season=Season.objects.by_date('2005-12-01'), division=divisions['Division 5NW'],
                                                         division_tables_url='http://www.east-leagues.co.uk/showdata/EML%20tables%200506.asp?division=5NW')
        ClubTeamSeasonParticipation.objects.get_or_create(team=clubteams['M2'], season=Season.objects.by_date('2006-12-01'), division=divisions['Division 5NW'],
                                                         division_tables_url='http://www.east-leagues.co.uk/showdata/EML%20tables%200607.asp?division=5NW')

        ClubTeamSeasonParticipation.objects.get_or_create(team=clubteams['M3'], season=Season.objects.by_date('2003-12-01'), division=divisions['Division 6NW'],
                                                         division_tables_url='http://www.east-leagues.co.uk/showdata/EML%20tables%200304.asp?division=6NW')
        ClubTeamSeasonParticipation.objects.get_or_create(team=clubteams['M3'], season=Season.objects.by_date('2004-12-01'), division=divisions['Division 6NW'],
                                                         division_tables_url='http://www.east-leagues.co.uk/showdata/EML%20tables%200405.asp?division=6NW')
        ClubTeamSeasonParticipation.objects.get_or_create(team=clubteams['M3'], season=Season.objects.by_date('2005-12-01'), division=divisions['Division 6NW'],
                                                         division_tables_url='http://www.east-leagues.co.uk/showdata/EML%20tables%200506.asp?division=6NW')
        ClubTeamSeasonParticipation.objects.get_or_create(team=clubteams['M3'], season=Season.objects.by_date('2006-12-01'), division=divisions['Division 6NW'],
                                                         division_tables_url='http://www.east-leagues.co.uk/showdata/EML%20tables%200607.asp?division=6NW')

        ClubTeamSeasonParticipation.objects.get_or_create(team=clubteams['L1'], season=Season.objects.by_date('2003-12-01'), division=divisions['Premier Division'])
        ClubTeamSeasonParticipation.objects.get_or_create(team=clubteams['L1'], season=Season.objects.by_date('2004-12-01'), division=divisions['Premier Division'])
        ClubTeamSeasonParticipation.objects.get_or_create(team=clubteams['L1'], season=Season.objects.by_date('2005-12-01'), division=divisions['Premier Division'])
        ClubTeamSeasonParticipation.objects.get_or_create(team=clubteams['L1'], season=Season.objects.by_date('2006-12-01'), division=divisions['Premier Division'])

        ClubTeamSeasonParticipation.objects.get_or_create(team=clubteams['Indoor'], season=Season.objects.by_date('2008-12-01'), cup=cups['Indoor Cup'])
        ClubTeamSeasonParticipation.objects.get_or_create(team=clubteams['Indoor'], season=Season.objects.by_date('2010-12-01'), cup=cups['Indoor Cup'])

    @staticmethod
    def add_matchaward_prerequisites():
        MatchAward.objects.get_or_create(name=MatchAward.MOM)
        MatchAward.objects.get_or_create(name=MatchAward.LOM)

    @staticmethod
    def sanitise(content):
        #content = bytearray(content).decode('utf-8')
        #content = content.replace('\r\n', '\n')
        #content = content.replace('\n\r', '\n')
        #content = content.replace('\r', '\n')
        # @todo sanitise; we have &entities; <elements> inconsistencies ...
        return content
