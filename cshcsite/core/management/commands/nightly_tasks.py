""" Management command that automates tasks that need to run on a
    periodic basis (typically daily).

    This command is run on the production site by a cronjob.

    Usage:
    python manage.py nightly_tasks
"""

from datetime import timedelta
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from matches.models import GoalKing
from competitions.models import Season, DivisionResult
from teams.stats import update_southerners_stats_for_season
from opposition.stats import update_all_club_stats
from teams.models import ClubTeamSeasonParticipation
from teams import league_scraper
from teams.stats import update_participation_stats_for_season
from training.models import TrainingSession

# To run:
# cron 0 2 * * * python /home/rgagarrett/new_site/repo/cshcsite/manage.py nightly_tasks >/dev/null

class Command(BaseCommand):
    """ Management command to execute various tasks that need to be run
        each day.
    """

    def handle(self, *args, **options):
        errors = []
        season = Season.current()

        try:
            # Update goal king
            GoalKing.update_for_season(season)
        except Exception as e:
            errors.append("Failed to update Goal-King: {}".format(e))

        try:
            # Update Southerners league
            update_southerners_stats_for_season(season)
        except Exception as e:
            errors.append("Failed to update Southerners League: {}".format(e))

        try:
            # Update opposition stats
            update_all_club_stats()
        except Exception as e:
            errors.append("Failed to update Opposition Club Stats: {}".format(e))

        try:
            # Update ClubTeamSeasonParticipation stats
            update_participation_stats_for_season(season)
        except Exception as e:
            errors.append("Failed to update Club Team Season Participation Stats: {}".format(e))

        # Scrape league tables
        participations = ClubTeamSeasonParticipation.objects.current().select_related('team', 'division')

        for participation in participations:
            try:
                DivisionResult.objects.league_table(season=season, division=participation.division).delete()
                try:
                    league_scraper.get_east_leagues_nw_division(participation.division_tables_url, participation.division, season)
                except Exception as e:
                    print "Failed to parse league table: {}".format(e)
            except Exception as e:
                errors.append("Failed to scrape league table from {}: {}".format(participation.division_tables_url, e))

        try:
            # Delete all training session entries from before yesterday (we don't care about
            # training sessions in the past)
            self.purge_training_sessions()
        except Exception as e:
            errors.append("Failed to purge training sessions: {}".format(e))

        if errors:
            send_mail("Nightly build task failed", "\n".join(errors), 'website@cambridgesouthhockeyclub.co.uk', ['website@cambridgesouthhockeyclub.co.uk'])


    def purge_training_sessions(self):
        """ Delete all training session entries from before a specified datetime,
            so they don't clog up the system.
        """
        yesterday = timezone.now() - timedelta(days=1)
        print "Purging all training sessions from before yesterday"
        TrainingSession.objects.before(yesterday).delete()
