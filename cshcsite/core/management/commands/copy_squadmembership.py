""" Management command used to copy all Squad Memberships from the previous
    season to the latest season.

    Usage:
    python manage.py copy_squadmembership
"""

from optparse import make_option
from django.core.management.base import BaseCommand
from members.models import SquadMembership
from competitions.models import Season


class Command(BaseCommand):
    """ Management command used to copy all Squad Memberships from the previous
        season to the latest season.
    """
    option_list = BaseCommand.option_list + (
        make_option('--sim',
                    action='store_true',
                    dest='simulate',
                    default=False,
                    help='Test run (doesn\'t actually save any copied models)'),
        )

    def handle(self, *args, **options):
        season = Season.objects.latest()
        prev_season = Season.objects.previous(season)

        if SquadMembership.objects.by_season(season).exists():
            print "ERROR: SquadMembership entries already exist for {0}. To run this command, first delete all SquadMembership entries for {0}".format(season)
            return

        prev_memberships = SquadMembership.objects.by_season(prev_season)

        for membership in prev_memberships:
            membership_copy = SquadMembership(season=season,
                                              member=membership.member,
                                              team=membership.team)
            if not options['simulate']:
                membership_copy.save()
            else:
                print "Saving new squad membership: {}".format(membership_copy)
