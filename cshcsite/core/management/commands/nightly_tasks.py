from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from matches.models import GoalKing
from competitions.models import Season, DivisionResult
from teams.stats import update_clubstats_for_season
from opposition.stats import update_all_club_stats
from teams.models import ClubTeamSeasonParticipation
from teams import league_scraper

# To run:
# cron 0 2 * * * python /home/rgagarrett/new_site/repo/cshcsite/manage.py nightly_tasks >/dev/null

class Command(BaseCommand):
    def handle(self, *args, **options):
        errors = []
        season = Season.current()

        try:
            # Update goal king
            GoalKing.update_for_season(season)
        except Exception as e:
            errors.add("Failed to update Goal-King: {}".format(e))

        try:
            # Update Southerners league
            update_clubstats_for_season(season)
        except Exception as e:
            errors.add("Failed to update Southerners League: {}".format(e))

        try:
            # Update opposition stats
            update_all_club_stats()
        except Exception as e:
            errors.add("Failed to update Opposition Club Stats: {}".format(e))

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
                errors.add("Failed to scrape league table from {}: {}".format(participation.division_tables_url, e))

        if errors:
            send_mail("Nightly build task failed", "\n".join(errors), 'website@cambridgesouthhockeyclub.co.uk', ['website@cambridgesouthhockeyclub.co.uk'])
