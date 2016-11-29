""" Various classes/code related to member statistics.

    These statistics are used by Django views and displayed on the
    member's profile page.

    They are not currently cached in a database table (like other stats,
    e.g. ClubStats) as they can still be calculated quickly enough 'live'.
    This situation may change in the future - in which case they should
    be dealt with in a similar manner to ClubStats.
"""

from matches.models import Match
from awards.models import MatchAward


class MatchesStat(object):
    """ Represents a member's match statistics.

        These statistics are agnostic of the context - it could be for a single season
        or all seasons or for a particular team, etc.

        Typically this is used to represent one type of fixture (e.g. League matches)
    """

    def __init__(self, is_total):
        # True if this instance represents a total of all seasons
        self.is_total = is_total
        # Total number of appearances
        self.appearances = 0
        # Total number of goals scored
        self.goals = 0
        # Totoal number of (team) clean sheets kept
        self.clean_sheets = 0

    def add_appearance(self, appearance):
        """ Add statistics from the specified appearance to the accumulated
            member match stats.
        """
        assert not self.is_total
        self.appearances += 1
        self.goals += appearance.goals
        if appearance.match.opp_score == 0:
            self.clean_sheets += 1

    def accumulate(self, matches_stat):
        """ Add the specified match statistics to the running totals"""
        assert self.is_total
        self.appearances += matches_stat.appearances
        self.goals += matches_stat.goals
        self.clean_sheets += matches_stat.clean_sheets


class SeasonMatchesStat(object):
    """ Represents all a player's match stats for a season.
        Contains separate League, Cup and Friendly stats as well as awards stats.
    """
    def __init__(self, season=None):
        # The season these stats apply to. None for a total.
        self.season = season
        # Total number of Man of the Match awards won
        self.mom = 0
        # Total number of Lemon of the Match awards won
        self.lom = 0
        # A dictionary of MatchesStats, keyed by fixture type
        self._stats = {}
        self._stats[Match.FIXTURE_TYPE.League] = MatchesStat(self.is_total())
        self._stats[Match.FIXTURE_TYPE.Cup] = MatchesStat(self.is_total())
        self._stats[Match.FIXTURE_TYPE.Friendly] = MatchesStat(self.is_total())
        self._stats['All'] = MatchesStat(self.is_total())

    def league(self):
        """ Returns a MatchesStats specific to League fixtures"""
        return self._stats[Match.FIXTURE_TYPE.League]

    def cup(self):
        """ Returns a MatchesStats specific to Cup fixtures"""
        return self._stats[Match.FIXTURE_TYPE.Cup]

    def friendly(self):
        """ Returns a MatchesStats specific to Friendly fixtures"""
        return self._stats[Match.FIXTURE_TYPE.Friendly]

    def all(self):
        """ Returns a MatchesStats for all fixtures"""
        return self._stats['All']

    def is_total(self):
        """ Returns True if this instance represents an accumulating total"""
        return self.season == None

    def add_appearance(self, appearance):
        """ Add statistics from the specified appearance to the match stats"""
        assert not self.is_total()
        self._stats[appearance.match.fixture_type].add_appearance(appearance)
        self._stats['All'].add_appearance(appearance)

    def add_award(self, award_winner):
        """ Adds the specified MatchAward to the member's season match stats"""
        assert not self.is_total()
        if award_winner.award.name == MatchAward.MOM:
            self.mom += 1
        elif award_winner.award.name == MatchAward.LOM:
            self.lom += 1

    def accumulate(self, season_matches_stat):
        """ Add the specified match statistics to the running totals"""
        assert self.is_total()
        self.mom += season_matches_stat.mom
        self.lom += season_matches_stat.lom
        for key, value in season_matches_stat._stats.items():
            self._stats[key].accumulate(value)


class SeasonTeamStat(object):
    """ Represents all a player's team stats for a season.
        Contains the total number of appearances for each team for a season.
    """
    def __init__(self, season=None):
        # The season these stats apply to. None for a total.
        self.season = season
        # A dictionary for each team (must be keyed on the slug of the team)
        self._appearances = {}
        self._appearances['m1'] = {"id": None, "count": 0}
        self._appearances['m2'] = {"id": None, "count": 0}
        self._appearances['m3'] = {"id": None, "count": 0}
        self._appearances['m4'] = {"id": None, "count": 0}
        self._appearances['m5'] = {"id": None, "count": 0}
        self._appearances['l1'] = {"id": None, "count": 0}
        self._appearances['l2'] = {"id": None, "count": 0}
        self._appearances['l3'] = {"id": None, "count": 0}
        self._appearances['mixed'] = {"id": None, "count": 0}
        self._appearances['indoor'] = {"id": None, "count": 0}
        self._appearances['vets'] = {"id": None, "count": 0}

    def m1_appearances(self):
        """ Returns the total number of appearances for the Men's 1sts"""
        return self._appearances['m1']

    def m2_appearances(self):
        """ Returns the total number of appearances for the Men's 2nds"""
        return self._appearances['m2']

    def m3_appearances(self):
        """ Returns the total number of appearances for the Men's 3rds"""
        return self._appearances['m3']

    def m4_appearances(self):
        """ Returns the total number of appearances for the Men's 4ths"""
        return self._appearances['m4']

    def m5_appearances(self):
        """ Returns the total number of appearances for the Men's 5ths"""
        return self._appearances['m5']

    def l1_appearances(self):
        """ Returns the total number of appearances for the Ladies 1sts"""
        return self._appearances['l1']

    def l2_appearances(self):
        """ Returns the total number of appearances for the Ladies 2nds"""
        return self._appearances['l2']

    def l3_appearances(self):
        """ Returns the total number of appearances for the Ladies 3rds"""
        return self._appearances['l3']

    def mix_appearances(self):
        """ Returns the total number of appearances for the Mixed team"""
        return self._appearances['mixed']

    def indoor_appearances(self):
        """ Returns the total number of appearances for the Indoor team"""
        return self._appearances['indoor']

    def vets_appearances(self):
        """ Returns the total number of appearances for the Vets team"""
        return self._appearances['vets']

    def is_total(self):
        """ Returns True if this instance represents an accumulating total"""
        return self.season == None

    def add_appearance(self, appearance):
        """ Adds the specified appearance to the appropriate team's running total"""
        assert not self.is_total()
        self._appearances[appearance.match.our_team.slug]["id"] = appearance.match.our_team.id
        self._appearances[appearance.match.our_team.slug]["count"] += 1

    def accumulate(self, season_team_stat):
        """ Add the specified team statistics to the running totals"""
        assert self.is_total()
        for key, value in season_team_stat._appearances.items():
            self._appearances[key]["count"] += value["count"]


class SeasonSuccessStat(object):
    """ Represents a member's success record (played, won, lost etc) for a particular season.
    """
    def __init__(self, season=None):
        # The season these stats apply to. None for a total.
        self.season = season
        # Total games played
        self.played = 0
        # Total games won
        self.won = 0
        # Total games drawn
        self.drawn = 0
        # Total games lost
        self.lost = 0
        # Total (team) goals scored - used to calculate an average per game
        self.total_goals_for = 0
        # Total (team) goals against - used to calculate an average per game
        self.total_goals_against = 0

    def avg_goals_for(self):
        """ Returns the average number of goals scored per game in matches this member played in"""
        if self.played == 0:
            return 0.0

        return float(self.total_goals_for) / float(self.played)

    def avg_goals_against(self):
        """ Returns the average number of goals scored per game by the opposition in matches
            this member played in.
        """
        if self.played == 0:
            return 0.0

        return float(self.total_goals_against) / float(self.played)

    def avg_points(self):
        """ Returns the average number of points per game in matches this member played in"""
        if self.played == 0:
            return 0.0

        return float(self.total_points()) / float(self.played)

    def total_points(self):
        """ Returns the total number of points accumulated in matches this member played in"""
        return ((Match.POINTS_FOR_WIN * self.won) +
                (Match.POINTS_FOR_DRAW * self.drawn) +
                (Match.POINTS_FOR_LOSS * self.lost))

    def is_total(self):
        """ Returns True if this instance represents an accumulating total"""
        return self.season == None

    def add_match(self, match):
        """ Adds the statistics from the specified match to the running totals"""
        assert not self.is_total()
        self.played += 1
        if match.was_won():
            self.won += 1
        elif match.was_lost():
            self.lost += 1
        else:
            self.drawn += 1
        self.total_goals_for += match.our_score
        self.total_goals_against += match.opp_score

    def accumulate(self, season_success_stat):
        """ Add the specified success record statistics to the running totals"""
        assert self.is_total()
        self.played += season_success_stat.played
        self.won += season_success_stat.won
        self.lost += season_success_stat.lost
        self.drawn += season_success_stat.drawn
        self.total_goals_for += season_success_stat.total_goals_for
        self.total_goals_against += season_success_stat.total_goals_against


class MemberSeasonStat(object):
    """ Represents all a member's statistics for a particular season"""

    def __init__(self, season=None):
        # The season these stats apply to. None for a total.
        self.season = season
        # Match stats
        self.matches = SeasonMatchesStat(season)
        # Team stats
        self.teams = SeasonTeamStat(season)
        # Success record stats
        self.success = SeasonSuccessStat(season)

    def is_total(self):
        """ Returns True if this instance represents an accumulating total"""
        return self.season == None

    def add_appearance(self, appearance):
        """ Adds statistics from the specified appearance to the running totals"""
        assert not self.is_total()
        self.matches.add_appearance(appearance)
        self.teams.add_appearance(appearance)
        self.success.add_match(appearance.match)

    def accumulate(self, member_season_stat):
        """ Add the specified member season statistics to the running totals"""
        assert self.is_total()
        self.matches.accumulate(member_season_stat.matches)
        self.teams.accumulate(member_season_stat.teams)
        self.success.accumulate(member_season_stat.success)
