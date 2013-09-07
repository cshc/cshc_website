import os
import csv
import traceback
from django.core.management.base import BaseCommand
from django.conf import settings
from django.utils.timezone import get_current_timezone
from optparse import make_option
from datetime import datetime
from core.models import not_none_or_empty
from awards.models import EndOfSeasonAward, EndOfSeasonAwardWinner
from competitions.models import Season
from opposition.models import Club
from training.models import TrainingSession
from venues.models import Venue
from teams.models import TeamCaptaincy, ClubTeam, ClubTeamSeasonParticipation
from members.models import Member

IMPORT_DIR = 'import'

DATE_FORMAT = '%d/%m/%Y'    # e.g. '01/09/2009'
TIME_FORMAT = '%H:%M'    # e.g. '19:30'

class TeamCaptainCsv:

    def __init__(self, row):
        self.team = bytearray(row[0]).decode('utf-8')
        self.full_name = bytearray(row[1]).decode('utf-8')
        name = self.full_name.split(' ')
        self.first_name = name[0]
        self.last_name = ' '.join(name[1:])
        self.is_vice = bytearray(row[2]).decode('utf-8') == 'y'
        self.start = datetime.strptime(bytearray(row[3]).decode('utf-8'), DATE_FORMAT).date()


class DivPartCsv:

    def __init__(self, row):
        self.team = bytearray(row[0]).decode('utf-8')
        self.season = bytearray(row[1]).decode('utf-8')
        self.league_tables_url = bytearray(row[2]).decode('utf-8')
        self.fixtures_url = bytearray(row[3]).decode('utf-8')

class AwardsCsv:

    def __init__(self, row):
        self.award_name = bytearray(row[0]).decode('utf-8')
        self.year = bytearray(row[1]).decode('utf-8')
        self.season = "{}-{}".format(int(self.year)-1, self.year)
        self.winner = bytearray(row[2]).decode('utf-8')
        name = self.winner.split(' ')
        self.winner_first_name = name[0]
        self.winner_last_name = name[1]
        self.comment = bytearray(row[3]).decode('utf-8')
        self.goals_scored = bytearray(row[4]).decode('utf-8')


class TrainingSessionCsv:

    def __init__(self, row):
        self.description = bytearray(row[0]).decode('utf-8')
        self.date = datetime.strptime(bytearray(row[1]).decode('utf-8'), DATE_FORMAT).date()
        self.start = datetime.strptime(bytearray(row[2]).decode('utf-8'), TIME_FORMAT).time()
        self.datetime = datetime.combine(self.date, self.start).replace(tzinfo=get_current_timezone())
        self.duration = int(bytearray(row[3]).decode('utf-8'))
        self.venue = bytearray(row[4]).decode('utf-8')


class VenueCsv:

    def __init__(self, row):
        self.name = bytearray(row[0]).decode('utf-8')
        self.phone = bytearray(row[1]).decode('utf-8')
        self.addr1 = bytearray(row[2]).decode('utf-8')
        self.addr2 = bytearray(row[3]).decode('utf-8')
        self.addr3 = bytearray(row[4]).decode('utf-8')
        self.city = bytearray(row[5]).decode('utf-8')
        self.postcode = bytearray(row[6]).decode('utf-8')
        self.notes = bytearray(row[7]).decode('utf-8')



class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--sim',
                    action='store_true',
                    dest='simulate',
                    default=False,
                    help='Test run (doesn\'t actually save any imported data)'),
        )
    help = 'Import data from csv files'

    def handle(self, *args, **options):
        try:
            self._handle(*args, **options)
        except:
            traceback.print_exc()

    def _handle(self, *args, **options):
        filename = args[0]
        sim = options['simulate']
        if filename == 'team_captains.csv':
            Command.import_team_captains(filename, sim)
        elif filename == 'team_div_part.csv':
            Command.import_team_div_part(filename, sim)
        elif filename == 'end_of_season_awards.csv':
            Command.import_end_of_season_awards(filename, sim)
        elif filename == 'training.csv':
            Command.import_training_sessions(filename, sim)
        elif filename == 'venues.csv':
            Command.import_venue_details(filename, sim)
        else:
            print "ERROR: Unexpected filename: {}".format(filename)

    @staticmethod
    def import_team_captains(filename, sim):
        captains = Command.import_data(filename, sim, TeamCaptainCsv)

        if not sim:
            # Start with a blank canvas
            print "Deleting all existing team captaincy records"
            TeamCaptaincy.objects.all().delete()

        for captain in captains:
            try:
                member = Member.objects.get(first_name=captain.first_name, last_name=captain.last_name)
            except Member.DoesNotExist:
                print "Member '{}' not found - skipped".format(captain.full_name)
            else:
                team = ClubTeam.objects.get(slug=captain.team)
                captaincy = TeamCaptaincy(member=member, team=team, start=captain.start, is_vice=captain.is_vice)
                if not sim:
                    captaincy.save()
                print "Saved new team captainy: {}".format(captaincy)

    @staticmethod
    def import_team_div_part(filename, sim):
        div_parts = Command.import_data(filename, sim, DivPartCsv)

        for div_part in div_parts:
            team = ClubTeam.objects.get(slug=div_part.team)
            try:
                season = Season.objects.get(slug=div_part.season)
                p = ClubTeamSeasonParticipation.objects.get(team=team, season=season)
            except (ClubTeamSeasonParticipation.DoesNotExist, Season.DoesNotExist):
                print "ERROR: Could not find participation info for {} in {}".format(team, div_part.season)
            else:
                if not_none_or_empty(div_part.league_tables_url):
                    p.division_tables_url = div_part.league_tables_url
                if not_none_or_empty(div_part.fixtures_url):
                    p.division_fixtures_url = div_part.fixtures_url
                if not sim:
                    p.save()
                print "Saved new Division Participation info for {} in {}".format(team, season)

    @staticmethod
    def import_end_of_season_awards(filename, sim):
        awards = Command.import_data(filename, sim, AwardsCsv)

        for award in awards:
            try:
                season = Season.objects.get(slug=award.season)
            except Season.DoesNotExist:
                print "ERROR: Could not find season {} - skipped".format(award.season)
                continue
            try:
                aw = EndOfSeasonAward.objects.get(name=award.award_name)
            except EndOfSeasonAward.DoesNotExist:
                aw = EndOfSeasonAward(name=award.award_name)
                if not sim:
                    aw.save()
                print "Added End of Season Award: {}".format(aw)

            try:
                member = Member.objects.get(first_name=award.winner_first_name, last_name=award.winner_last_name)
            except:
                member = None
            try:
                if member:
                    award_winner = EndOfSeasonAwardWinner.objects.get(award=aw, member=member, season=season)
                else:
                    award_winner = EndOfSeasonAwardWinner.objects.get(award=aw, awardee=award.winner, season=season)
            except EndOfSeasonAwardWinner.DoesNotExist:
                if member:
                    award_winner = EndOfSeasonAwardWinner(award=aw, member=member, season=season, comment=award.comment)
                else:
                    award_winner = EndOfSeasonAwardWinner(award=aw, awardee=award.winner, season=season, comment=award.comment)

                if not_none_or_empty(award.goals_scored):
                    award_winner.comment += (award_winner.comment + " ({} goals)".format(award.goals_scored)).strip()
                if not sim:
                    award_winner.save()
                print "Added End of Season award winner: {}".format(award_winner)

    @staticmethod
    def import_training_sessions(filename, sim):
        sessions = Command.import_data(filename, sim, TrainingSessionCsv)

        for session in sessions:
            venue = Venue.objects.get(short_name=session.venue)
            try:
                sess = TrainingSession.objects.get(description=session.description, datetime=session.datetime)
            except TrainingSession.DoesNotExist:
                sess = TrainingSession(description=session.description, datetime=session.datetime, venue=venue)
                if not sim:
                    sess.save()
                print "Saved new training session: {}".format(sess)
            else:
                print "Skipped existing training session: {}".format(sess)

    @staticmethod
    def import_venue_details(filename, sim):
        venue_details = Command.import_data(filename, sim, VenueCsv)

        for details in venue_details:
            try:
                venue = Venue.objects.get(name=details.name)
            except Venue.DoesNotExist:
                print "ERROR: Could not find venue '{}'".format(details.name)
                continue
            else:
                venue.phone = details.phone
                venue.addr1 = details.addr1
                venue.addr2 = details.addr2
                venue.addr3 = details.addr3
                venue.addr_city = details.city
                venue.addr_postcode = details.postcode
                venue.notes = details.notes
                if not sim:
                    venue.save()
                print "Updated venue details for {}".format(venue.name)

    @staticmethod
    def import_data(filename, sim, cls):
        file_path = os.path.join(settings.SITE_ROOT, IMPORT_DIR, filename)
        results = []
        with open(file_path, 'rb') as source_file:
            reader = csv.reader(source_file)
            first_row = True
            for csv_row in reader:
                # Ignore the first row (field names)
                if first_row:
                    first_row = False
                    continue
                res = cls(csv_row)
                results.append(res)

        return results