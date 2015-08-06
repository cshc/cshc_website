""" Imports/syncs fixtures from a CSV file.

    Typically this is used at the start of a season
    to quickly create all the fixtures for the coming season.

    Usage: python manage.py import_fixtures fixtures.csv

    Note: the CSV file is generated from an Excel spreadsheet.
    Currently this module hard-codes a lot of details about the
    layout of this spreadsheet.

    DO NOT ALTER THE LAYOUT OF THE SPREADSHEET!

    Doing so will almost certainly break the import/sync functionality!

    However, if you do alter the spreadsheet layout, it should be relatively
    easy to modify the code in this module to work with the new layout.

"""
import csv
import os.path
import traceback
from datetime import datetime
from optparse import make_option
from django.core.management.base import BaseCommand
from django.db.models import Q
from matches.models import Match
from opposition.models import Team
from teams.models import ClubTeam
from venues.models import Venue
from competitions.models import Season

###############################################################################
# Hard-coded CSV layout details. If the spreadsheet layout changes, these
# will be the first things that need to change!

# For each team, the following columns are used:
OFFSET = {
    'buffer': 0,
    'fixture_type': 1,
    'home_away': 2,
    'opposition': 3,
    'venue': 4,
    'time': 5,
}

# Offset of the column containing dates
DATE_COL = 0

# Lookup table for fixture-types (all caps are converted to lower case prior to comparison)
MATCH_TYPE = {
    'f': Match.FIXTURE_TYPE.Friendly,
    'l': Match.FIXTURE_TYPE.League,
    'c': Match.FIXTURE_TYPE.Cup,
}

# Lookup table for home/away designations (all caps are converted to lower case prior to comparison)
HOME_AWAY = {
    'h': Match.HOME_AWAY.Home,
    'a': Match.HOME_AWAY.Away,
}

###############################################################################

class ParseException(Exception):
    """ Custom exception for parsing errors """
    pass


def print_usage():
    print "Usage: python manage.py import_fixtures <filename>"
    print ""
    print "Where: <filename> is the path to the fixtures CSV (comma-separated-values) file"


class Command(BaseCommand):
    """ Management command used to import a fixture list from a CSV file.
    """

    def __init__(self):
        super(Command, self).__init__()

    option_list = BaseCommand.option_list + (
        make_option('--sim',
                    action='store_true',
                    dest='simulate',
                    default=False,
                    help='Test run (doesn\'t actually save any Match models)'),
        )

    def handle(self, *args, **options):
        if len(args) != 1:
            print_usage()
            return

        # Check fixtures file argument
        file_path = args[0]
        if not os.path.isfile(file_path):
            print "ERROR: No such file '{}'".format(file_path)
            return

        simulate = options['simulate']

        with open(file_path, 'rb') as source_file:
            reader = csv.reader(source_file)

            # First cache references to the club teams
            try:
                club_teams = self._cache_teams(reader)
            except:
                traceback.print_exc()
                return

            # Then loop through the dates
            try:
                while True:
                    csv_row = reader.next()
                    date_field = csv_row[DATE_COL]
                    try:
                        fixture_date = datetime.strptime(date_field, "%d-%b-%y").date()
                    except:
                        if date_field != '':
                            print "ERROR: Could not parse date field: {}".format(date_field)
                        continue

                    # Get the season that corresponds to this date
                    try:
                        fixture_season = Season.objects.by_date(fixture_date)
                    except:
                        print "ERROR: Could not find season for date: {}".format(date_field)
                        continue

                    team_offset = DATE_COL + 1
                    # Process each team for this date. Some of the teams will not have matches - that's fine.
                    for club_team in club_teams:
                        self._parse_fixture(simulate, fixture_season, fixture_date, club_team, csv_row[team_offset:team_offset+len(OFFSET)])
                        team_offset += len(OFFSET)
            except StopIteration:
                pass    # We're done!
            except:
                traceback.print_exc()

    def _cache_teams(self, reader):
        """ Parse the second row of the file to extract the team names and then
            cache the corresponding ClubTeam model instances.

            Returns a list of dictionaries. Each dictionary contains 'name' and
            'team' keys.

            Note: The team names in the second row must *exactly* match the
                  team's 'short name' on the website.
        """
        club_teams = []
        reader.next()                   # Ignore first line (heading)
        team_names_row = reader.next()  # Second line contains the team names
        club_teams = [{'name': x, 'team': None} for x in team_names_row if x != '']

        if len(club_teams) < 1:
            raise ParseException("FATAL ERROR: Could not find team names on row 2")

        for team in club_teams:
            try:
                team['team'] = ClubTeam.objects.get(short_name=team['name'])
            except ClubTeam.DoesNotExist:
                raise ParseException("FATAL ERROR: Unrecognised team name: {}".format(team['name']))

        return club_teams

    def _parse_fixture(self, simulate, fixture_season, fixture_date, club_team, fields):
        """ Creates/updated a match model instance based on the relevant fields from the CSV file."""
        # Slight hack to decide whether the fixture is specified or not
        if fields[OFFSET['fixture_type']] == "":
            print "No match for {} on {}".format(club_team['name'], fixture_date)
            return

        team_name = club_team['name']
        our_team = club_team['team']
        fixture_type = fields[OFFSET['fixture_type']]
        opp_team_name = fields[OFFSET['opposition']]
        venue_name = fields[OFFSET['venue']]
        fixture_time_str = fields[OFFSET['time']]
        home_away = fields[OFFSET['home_away']]

        try:
            opp = Team.objects.get(name=opp_team_name)
        except Team.DoesNotExist:
            print "ERROR: Could not find opposition team with name '{}'".format(opp_team_name)
            return

        # Create or retrieve Match model (based on opposition team, our team and date)
        if not simulate:
            match, created = Match.objects.get_or_create(season=fixture_season, opp_team=opp, our_team=our_team, date=fixture_date)
        else:
            created = not Match.objects.filter(season=fixture_season, opp_team=opp, our_team=our_team, date=fixture_date).exists()
            match = Match(season=fixture_season, opp_team=opp, our_team=our_team, date=fixture_date)

        # Match home/away designation
        try:
            match.home_away = HOME_AWAY[home_away.lower()]
        except:
            print "ERROR: Invalid Home/Away designation '{}' for {} on {}".format(home_away, team_name, fixture_date)
            return

        # Match fixture type (League/Cup/Friendly)
        try:
            match.fixture_type = MATCH_TYPE[fixture_type.lower()]
        except:
            print "ERROR: Invalid fixture type designation '{}' for {} on {}".format(fixture_type, team_name, fixture_date)
            return

        # Match time (can be null)
        if fixture_time_str:
            try:
                match.time = datetime.strptime(fixture_time_str, "%H:%M").time()
            except:
                print "ERROR: Could not parse fixture time '{}' for {} on {}".format(fixture_time_str, team_name, fixture_date)
                return
        else:
            match.time = None


        # Match Venue (can be null)
        if venue_name.lower() == 'away' or (home_away.lower() == 'a' and venue_name.lower() == ''):
            match.venue = None
        else:
            try:
                name_q = Q(name=venue_name) | Q(short_name=venue_name)
                match.venue = Venue.objects.get(name_q)
            except Venue.DoesNotExist:
                print "ERROR: Could not find venue '{}' for {} on {}".format(venue_name, team_name, fixture_date)
                return

        if not simulate:
            match.save()

        print "{} {}".format("Created" if created else "Updated", match)


