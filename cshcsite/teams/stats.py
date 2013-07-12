import logging
from awards.models import MatchAward
from matches.models import Match
from competitions.models import Season
from models import Southerner

log = logging.getLogger(__name__)

def update_clubstats_for_season(season):
    """Updates the Southerner entries for the specified season"""
    log.info("Updating Southerners League stats for {}".format(season))
    s_entries = Southerner.objects.by_season(season)

    # A dictionary for Southerner entries, keyed by the team id
    s_lookup = {}

    # Reset all the entries
    for s in s_entries:
        s.reset()
        s_lookup[s.team_id] = s

    matches = Match.objects.by_season(season).results().filter(ignore_for_southerners=False, our_team__southerners=True, our_score__isnull=False, opp_score__isnull=False).select_related('our_team', 'season')

    for match in matches:
        if not s_lookup.has_key(match.our_team_id):
            s_lookup[match.our_team_id] = Southerner(team=match.our_team, season=match.season)
        s_lookup[match.our_team_id].add_match(match)

    for key, value in s_lookup.iteritems():
        value.save()



class SquadMember(object):
    """Represents statistics about a squad member"""

    def __init__(self, member):
        self.member = member
        self.goals = 0
        self.appearances = 0
        self.clean_sheets = 0
        self.mom = 0
        self.lom = 0

    def add_appearance(self, appearance):
        """Add the specified appearance to the squad member's stats"""
        self.appearances += 1
        self.goals += appearance.goals
        if appearance.match.opp_score == 0:
            self.clean_sheets += 1

    def add_award(self, award):
        """Add the specified award to the squad member's stats"""
        if award.name == MatchAward.MOM:
            self.mom += 1
        elif award.name == MatchAward.LOM:
            self.lom += 1