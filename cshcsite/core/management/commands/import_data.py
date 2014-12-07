import os
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
from .command_utils import import_csv_data

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
        self.existing_name = bytearray(row[0]).decode('utf-8')
        self.full_name = bytearray(row[1]).decode('utf-8')
        self.short_name = bytearray(row[2]).decode('utf-8')
        self.url = bytearray(row[3]).decode('utf-8')
        self.is_home = bytearray(row[4]).decode('utf-8') == 'Yes'
        self.phone = bytearray(row[5]).decode('utf-8')
        self.addr1 = bytearray(row[6]).decode('utf-8')
        self.addr2 = bytearray(row[7]).decode('utf-8')
        self.addr3 = bytearray(row[8]).decode('utf-8')
        self.city = bytearray(row[9]).decode('utf-8')
        self.postcode = bytearray(row[10]).decode('utf-8')
        self.notes = bytearray(row[11]).decode('utf-8')


class ClubCsv:

    def __init__(self, row):
        self.name = bytearray(row[0]).decode('utf-8')
        self.website = bytearray(row[1]).decode('utf-8')


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--sim',
                    action='store_true',
                    dest='simulate',
                    default=False,
                    help='Test run (doesn\'t actually save any imported data)'),
        make_option('--all',
                    action='store_true',
                    dest='all',
                    default=False,
                    help='Import all data)'),
        )

    help = 'Import data from csv files'

    def handle(self, *args, **options):
        try:
            self._handle(*args, **options)
        except:
            traceback.print_exc()

    def _handle(self, *args, **options):
        sim = options['simulate']
        all = options['all']
        if not all:
            filename = args[0]

        if all or filename == 'team_captains.csv':
            Command.import_team_captains(sim)
        if all or filename == 'team_div_part.csv':
            Command.import_team_div_part(sim)
        if all or filename == 'end_of_season_awards.csv':
            Command.import_end_of_season_awards(sim)
        if all or filename == 'training.csv':
            Command.import_training_sessions(sim)
        if all or filename == 'club_details.csv':
            Command.import_club_details(sim)
        if all or filename == 'venues.csv':
            #Command.import_venue_details(sim)
            print "SKIPPING VENUS (BUGGY)"

    @staticmethod
    def import_team_captains(sim):
        filename = 'team_captains.csv'
        file_path = os.path.join(settings.SITE_ROOT, IMPORT_DIR, filename)
        captains = import_csv_data(file_path, TeamCaptainCsv)

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
    def import_team_div_part(sim):
        filename = 'team_div_part.csv'
        file_path = os.path.join(settings.SITE_ROOT, IMPORT_DIR, filename)
        div_parts = import_csv_data(file_path, DivPartCsv)

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
    def import_end_of_season_awards(sim):
        filename = 'end_of_season_awards.csv'
        file_path = os.path.join(settings.SITE_ROOT, IMPORT_DIR, filename)
        awards = import_csv_data(file_path, AwardsCsv)

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
    def import_training_sessions(sim):
        filename = 'training.csv'
        file_path = os.path.join(settings.SITE_ROOT, IMPORT_DIR, filename)
        sessions = import_csv_data(file_path, TrainingSessionCsv)

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
    def import_venue_details(sim):
        filename = 'venues.csv'
        file_path = os.path.join(settings.SITE_ROOT, IMPORT_DIR, filename)
        venue_details = import_csv_data(file_path, VenueCsv)

        for details in venue_details:
            try:
                venue = Venue.objects.get(name=details.full_name)
            except Venue.DoesNotExist:
                try:
                    venue = Venue.objects.get(name=details.existing_name)
                except Venue.DoesNotExist:
                    print "WARNING: Could not find venue '{}'. Creating now".format(details.existing_name)
                    venue = Venue()
            venue.name = details.full_name
            # TEMP: ignore short_name
            #venue.short_name = details.short_name
            venue.url = details.url
            venue.is_home = details.is_home
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
    def import_club_details(sim):
        filename = 'club_details.csv'
        file_path = os.path.join(settings.SITE_ROOT, IMPORT_DIR, filename)
        club_details = import_csv_data(file_path, ClubCsv)

        for details in club_details:
            try:
                club = Club.objects.get(name=details.name)
            except Club.DoesNotExist:
                print "WARNING: Could not find club '{}'. Creating now".format(details.name)
                club = Club()
            club.name = details.name
            club.website = details.website
            if not sim:
                club.save()
            print "Updated club details for {}".format(club.name)