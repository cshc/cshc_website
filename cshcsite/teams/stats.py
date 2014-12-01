""" Utility methods for calculating team statistics.
"""

import logging
from awards.models import MatchAward
from matches.models import Match
from teams.models import Southerner, ClubTeamSeasonParticipation

LOG = logging.getLogger(__name__)

def update_southerners_stats_for_season(season):
    """Updates the Southerner entries for the specified season"""
    LOG.info("Updating Southerners League stats for {}".format(season))
    s_entries = Southerner.objects.by_season(season)

    # A dictionary for Southerner entries, keyed by the team id
    s_lookup = {}

    # Reset all the entries
    for entry in s_entries:
        entry.reset()
        s_lookup[entry.team_id] = entry

    match_qs = Match.objects.by_season(season).results()
    match_qs = match_qs.filter(ignore_for_southerners=False, our_team__southerners=True,
                               our_score__isnull=False, opp_score__isnull=False)
    match_qs = match_qs.select_related('our_team', 'season')

    for match in match_qs:
        if not s_lookup.has_key(match.our_team_id):
            s_lookup[match.our_team_id] = Southerner(team=match.our_team, season=match.season)
        s_lookup[match.our_team_id].add_match(match)

    for _, value in s_lookup.iteritems():
        value.save()


def update_participation_stats_for_season(season):
    """ Updates the stats fields embedded in all ClubTeamSeasonParticipation
        model instances.
    """
    participations = ClubTeamSeasonParticipation.objects.by_season(season).select_related('team')
    for participation in participations:
        update_participation_stats(participation)


# Note - the following two methods can't be instance methods of the
# ClubTeamSeasonParticipation model as it would result in a circular reference
# between Match and ClubTeamSeasonParticipation.

def update_participation_stats(participation):
    """ Updates participation stats.
    """
    LOG.info("Updating Club Team Season Participation stats for {}".format(participation))
    participation.reset()

    # We just want the member id, the match team, the number of goals scored (and own goals)
    match_qs = Match.objects.by_season(participation.season)
    match_qs = match_qs.filter(our_team=participation.team, our_score__isnull=False,
                               opp_score__isnull=False)

    for match in match_qs:
        add_match(participation, match)

    # Save the updated entries back to the database
    participation.save()


def add_match(participation, match):
    """ Adds the statistics from the given match to the running totals
        within the ClubTeamSeasonParticipation instance.
    """
    if match.fixture_type == Match.FIXTURE_TYPE.Friendly:
        participation.friendly_played += 1
        if match.was_won():
            participation.friendly_won += 1
        elif match.was_lost():
            participation.friendly_lost += 1
        else:
            participation.friendly_drawn += 1
        participation.friendly_goals_for += match.our_score
        participation.friendly_goals_against += match.opp_score
    elif match.fixture_type == Match.FIXTURE_TYPE.Cup:
        participation.cup_played += 1
        if match.was_won():
            participation.cup_won += 1
        elif match.was_lost():
            participation.cup_lost += 1
        else:
            participation.cup_drawn += 1
        participation.cup_goals_for += match.our_score
        participation.cup_goals_against += match.opp_score
    else:
        participation.league_played += 1
        if match.was_won():
            participation.league_won += 1
        elif match.was_lost():
            participation.league_lost += 1
        else:
            participation.league_drawn += 1
        participation.league_goals_for += match.our_score
        participation.league_goals_against += match.opp_score


class SquadMember(object):
    """ Represents statistics about a squad member"""

    def __init__(self, member):
        self.member = member
        self.goals = 0
        self.appearances = 0
        self.clean_sheets = 0
        self.mom = 0
        self.lom = 0

    def add_appearance(self, appearance):
        """ Add the specified appearance to the squad member's stats"""
        self.appearances += 1
        self.goals += appearance.goals
        if appearance.match.opp_score == 0:
            self.clean_sheets += 1

    def add_award(self, award):
        """ Add the specified award to the squad member's stats"""
        if award.name == MatchAward.MOM:
            self.mom += 1
        elif award.name == MatchAward.LOM:
            self.lom += 1
