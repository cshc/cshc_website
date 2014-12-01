""" Management command used to copy all Squad Memberships from the previous
    season to the specified season.

    Usage:
    python manage.py copy_squadmembership <season-slug>
"""

from optparse import make_option
from django.core.management.base import BaseCommand
from members.models import SquadMembership
from competitions.models import Season


class Command(BaseCommand):
    """ Management command used to copy all Squad Memberships from the previous
        season to the specified season.
    """
    option_list = BaseCommand.option_list + (
        make_option('--sim',
                    action='store_true',
                    dest='simulate',
                    default=False,
                    help='Test run (doesn\'t actually save any copied models)'),
        )

    def handle(self, *args, **options):
        if len(args) != 1:
            print "ERROR: You must specify the season for which to populate squad membership entries"
            print "       E.g. 'python manage.py copy_squadmembership 2012-2013'"
            return
        season_slug = args[0]
        season = Season.objects.get(slug=season_slug)
        prev_season = Season.objects.previous(season)

        prev_memberships = SquadMembership.objects.by_season(prev_season)

        for membership in prev_memberships:
            membership_copy = SquadMembership(season=season,
                                              member=membership.member,
                                              team=membership.team)
            if not options['simulate']:
                membership_copy.save()
            else:
                print "Saving new squad membership: {}".format(membership_copy)
