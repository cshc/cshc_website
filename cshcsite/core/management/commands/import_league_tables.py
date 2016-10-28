import os
import csv
import traceback
from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option
from .command_utils import import_csv_data
from core.models import TeamGender
from opposition.models import Team
from teams.models import ClubTeam
from competitions.models import Season, League, Division, DivisionResult

IMPORT_DIR = 'import'
SUBDIR = 'league_tables'

class TeamCsv(object):

    def __init__(self, row):
        self.team = bytearray(row[0]).decode('utf-8')
        self.played = int(bytearray(row[1]).decode('utf-8'))
        self.won = int(bytearray(row[2]).decode('utf-8'))
        self.drawn = int(bytearray(row[3]).decode('utf-8'))
        self.lost = int(bytearray(row[4]).decode('utf-8'))
        self.gf = int(bytearray(row[5]).decode('utf-8'))
        self.ga = int(bytearray(row[6]).decode('utf-8'))
        self.gd = int(bytearray(row[7]).decode('utf-8'))
        self.pts = int(bytearray(row[8]).decode('utf-8'))
        self.notes = bytearray(row[9]).decode('utf-8')
        self.position = None

    def __unicode__(self):
        return unicode("{}".format(self.__dict__))

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--sim',
                    action='store_true',
                    dest='simulate',
                    default=False,
                    help='Test run (doesn\'t actually save any imported data)'),
        )
    help = 'Import league tables from csv files'

    def handle(self, *args, **options):
        try:
            self._handle(*args, **options)
        except:
            traceback.print_exc()

    def _handle(self, *args, **options):
        sim = options['simulate']

        root_folder = os.path.join(settings.SITE_ROOT, IMPORT_DIR, SUBDIR)

        files_to_import = [f for f in os.listdir(root_folder) if os.path.isfile(os.path.join(root_folder, f))]
        errors = []
        for f in files_to_import:
            table_details = f.lstrip('Old League Tables - ').rstrip('.csv').split(',')
            league_name = table_details[0].strip()
            g = table_details[1].strip()
            gender = TeamGender.Mens if g == 'Mens' else TeamGender.Ladies if g == 'Ladies' else TeamGender.Mixed
            division_name = table_details[2].strip()
            season_slug = table_details[3].strip()
            league = League.objects.get(name=league_name)
            try:
                div = Division.objects.get(league=league, name=division_name, gender=gender)
            except Division.DoesNotExist:
                errors.append("ERROR: Could not find division: {} {} ({})".format(league, division_name, gender))
                continue
            try:
                season = Season.objects.get(slug=season_slug)
            except Season.DoesNotExist:
                errors.append("ERROR: Could not find season {}".format(season_slug))
                continue
            teams = import_csv_data(os.path.join(root_folder, f), TeamCsv)

            pos = 0
            for team in teams:
                pos += 1
                team.position = pos
                team_name = team.team
                try:
                    our_team = ClubTeam.objects.get(slug=team_name.lower())
                    opp_team = None
                except ClubTeam.DoesNotExist:
                    try:
                        words = team_name.split()
                        if gender not in words:
                            words.insert(-1, gender)
                        team_name = " ".join(words)
                        opp_team = Team.objects.get(name=team_name)
                        our_team = None
                    except Team.DoesNotExist:
                        errors.append("ERROR: Could not find team '{}' ({} {} - {}, {})".format(team_name, league_name, division_name, gender, season))
                        continue
                div_result, c = DivisionResult.objects.get_or_create(season=season, division=div, position=team.position,
                    defaults={'our_team':our_team, 'opp_team':opp_team})
                div_result.played = team.played
                div_result.won = team.won
                div_result.drawn = team.drawn
                div_result.lost = team.lost
                div_result.goals_for = team.gf
                div_result.goals_against = team.ga
                div_result.goal_difference = team.gd
                div_result.points = team.pts
                div_result.notes = team.notes
                try:
                    if not sim:
                        div_result.save()
                    print "Saving division result: {}".format(div_result)
                except:
                    errors.append("Failed to save result for {} {} {} {}".format(team_name, division_name, gender, season))

        for error in errors:
            print error