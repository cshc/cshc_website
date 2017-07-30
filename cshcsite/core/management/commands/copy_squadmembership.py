""" Management command used to copy all Squad Memberships from the previous
    season to the latest season.

    Usage:
    python manage.py copy_squadmembership
"""

import traceback
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

    def _handle(self, *args, **options):
        season = Season.objects.latest()
        prev_season = Season.objects.previous(season)

        memberships = SquadMembership.objects.by_season(season)
        membership_count = memberships.count()  # Save has the quirky effect of updating the original object (memberships), so cache the 'before' count.

        if not options ['simulate'] and memberships.exists():
            print "ERROR: SquadMembership entries already exist for {0}. To run this command (non-simulated), first delete all SquadMembership entries for {0}".format(season)
            return -1

        prev_memberships = SquadMembership.objects.by_season(prev_season)
        
        for membership in prev_memberships:
            membership_copy = SquadMembership(season=season,
                                              member=membership.member,
                                              team=membership.team)
            if not options['simulate']:
                membership_copy.save()
            else:
                print "Would save new squad membership: {}".format(membership_copy)

        updated_membership_count = SquadMembership.objects.by_season(season).count()
        print "Squad memberships summary: Current season: %d (was %d before script); previous season: %d" % (updated_membership_count, membership_count, prev_memberships.count())
        return 0

    def handle(self, *args, **options):
        try:
            result = self._handle(*args, **options)
            if result == 0:
                print "OK"
            else:
                print "ERROR: Return status (%d)" % (result)
        except:
            print "ERROR: Caught exception..."
            traceback.print_exc()
