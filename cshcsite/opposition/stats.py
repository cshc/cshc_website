""" Helper methods for collecting statistics on opposition clubs.
"""

import logging
from matches.models import Match
from opposition.models import Club, ClubStats

LOG = logging.getLogger(__name__)


def update_all_club_stats():
    """ Updates all club stats.

        Returns an array of 'totals' ClubStats instances,
        one per club.
    """
    LOG.info("Updating all Club stats")
    clubs = Club.objects.only('pk', 'name')

    clubstats = []
    for club in clubs:
        club_totals = update_club_stats_for_club(club)
        clubstats.append(club_totals)

    return clubstats


def update_club_stats_for_club(club):
    """ Updates the Club Stats entries for the specified opposition club.

        Returns the totals ClubStat instance for the specified club.
    """
    LOG.info("Updating Club stats for {}".format(club))
    s_entries = ClubStats.objects.filter(club=club)

    # A dictionary for Club Stats entries, keyed by the team id
    s_lookup = {}

    totals = None
    # Reset all the entries
    for stat in s_entries:
        stat.reset()
        if not stat.is_club_total():
            s_lookup[stat.team_id] = stat
        else:
            totals = stat

    # Get all match results against this club
    matches = Match.objects.results().filter(our_team__rivals=True, our_score__isnull=False,
        opp_score__isnull=False, opp_team__club=club).select_related('our_team', 'opp_team__club')

    # Update with match stats
    for match in matches:
        if not s_lookup.has_key(match.our_team_id):
            s_lookup[match.our_team_id] = ClubStats(team=match.our_team, club=club)
        s_lookup[match.our_team_id].add_match(match)

    # Update totals
    if totals is None:
        totals = ClubStats(club=club)
    for stat in s_lookup.values():
        totals.accumulate_stats(stat)
    totals.save()

    # Save all updated stats back to the database
    for _, value in s_lookup.iteritems():
        value.save()

    return totals
