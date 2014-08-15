"""
Generic, reusable functions that relate to members
"""

from awards.models import MatchAwardWinner, EndOfSeasonAwardWinner
from matches.models import Match
from members.models import CommitteeMembership


def get_recent_match_awards(member, count=3):
    """
    Gets a QuerySet of recent match awards for the specified member.

        - returns (no more than) the specified number of awards (default = 3)
        - result is ordered by most recent first
    """
    return MatchAwardWinner.objects.by_member(member).order_by('-match__date').select_related('award', 'member', 'match')[:count]


def get_recent_end_of_season_awards(member, count=3):
    """
    Gets a QuerySet of recent End of Season awards for the specified member.

        - returns (no more than) the specified number of awards (default = 3)
        - result is ordered by most recent first
    """
    return EndOfSeasonAwardWinner.objects.by_member(member).order_by('-season__start').select_related('award', 'member', 'season')[:count]


def get_recent_match_reports(member, count=3):
    """
    Gets a QuerySet of recent matches whose match reports were written by the specified member.

        - returns (no more than) the specified number of matches (default = 3)
        - result is ordered by most recent first
    """
    return Match.objects.by_report_author(member).order_by('-date', '-time')[:count]


def get_committee_positions(member):
    """
    Gets a QuerySet of all committee positions held for the specified member.

        - returns a QuerySet of CommitteeMembership models for the specified member.
        - result is ordered by most recent first
    """
    return CommitteeMembership.objects.by_member(member).order_by('-season__start').select_related('position', 'member', 'season')
