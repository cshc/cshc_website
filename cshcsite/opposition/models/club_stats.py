""" The ClubStats model represents the accumulative playing record
    of Cambridge South teams against another club.

    The data is used in the Opposition Clubs stats page.

    Note that for a particular opposition club, there will be multiple
    instances of ClubStats. One tracks the accumulative playing record
    of ALL Cambridge South teams and the others track the playing
    records of the individual Cambridge South teams against that club.

    Note: ClubStats are updated automatically via the nightly cronjob
    task. They should not be manually edited (and for this reason are
    not available on the admin interface).
"""

from django.db import models
from opposition.models.club import Club
from teams.models import ClubTeam


class ClubStatsManager(models.Manager):
    """Manager for the ClubStats model"""

    def totals(self):
        """Returns a list of all the club totals"""
        return self.get_query_set().select_related('club').filter(team__isnull=True)


class ClubStats(models.Model):
    """ Represents the playing record for Cambridge South teams against
        a particular opposition club.
    """

    team = models.ForeignKey(ClubTeam, null=True)
    """The Cambridge South team these stats relate to. Null for ALL teams."""

    club = models.ForeignKey(Club)
    """The opposition club these stats relate to."""

    home_won = models.PositiveSmallIntegerField("Home matches won", default=0)
    home_drawn = models.PositiveSmallIntegerField("Home matches drawn", default=0)
    home_lost = models.PositiveSmallIntegerField("Home matches lost", default=0)
    home_gf = models.PositiveSmallIntegerField("Home matches - goals for", default=0)
    home_ga = models.PositiveSmallIntegerField("Home matches - goals against", default=0)

    away_won = models.PositiveSmallIntegerField("Away matches won", default=0)
    away_drawn = models.PositiveSmallIntegerField("Away matches drawn", default=0)
    away_lost = models.PositiveSmallIntegerField("Away matches lost", default=0)
    away_gf = models.PositiveSmallIntegerField("Away matches - goals for", default=0)
    away_ga = models.PositiveSmallIntegerField("Away matches - goals against", default=0)

    objects = ClubStatsManager()

    class Meta:
        """ Meta-info for the ClubStats model."""
        app_label = 'opposition'
        ordering = ['club', 'team']

    @property
    def home_played(self):
        """Return the total number of home games played"""
        return self.home_won + self.home_drawn + self.home_lost

    @property
    def away_played(self):
        """Return the total number of away games played"""
        return self.away_won + self.away_drawn + self.away_lost

    @property
    def total_played(self):
        """Return the total number of games played (home and away)"""
        return self.home_played + self.away_played

    @property
    def total_won(self):
        """Return the total number of games won (home and away)"""
        return self.home_won + self.away_won

    @property
    def total_drawn(self):
        """Return the total number of games drawn (home and away)"""
        return self.home_drawn + self.away_drawn

    @property
    def total_lost(self):
        """Return the total number of games lost (home and away)"""
        return self.home_lost + self.away_lost

    @property
    def total_gf(self):
        """Return the total number of goals for (home and away)"""
        return self.home_gf + self.away_gf

    @property
    def total_ga(self):
        """Return the total number of goals against (home and away)"""
        return self.home_ga + self.away_ga

    @property
    def avg_gf(self):
        """Returns the average number of goals scored by our team per game against this club"""
        if self.total_played == 0:
            return 0.0
        return float(self.total_gf) / float(self.total_played)

    @property
    def avg_ga(self):
        """Returns the average number of goals scored by the opposition per game against this club"""
        if self.total_played == 0:
            return 0.0
        return float(self.total_ga) / float(self.total_played)

    @property
    def avg_gd(self):
        """Returns the average goal difference per game against this club"""
        return self.avg_gf - self.avg_ga

    @property
    def avg_points(self):
        """Returns the average number of points per match against this club"""
        if self.total_played == 0:
            return 0.0
        return float(self.total_won * 3 + self.total_drawn * 1) / float(self.total_played)

    def is_club_total(self):
        """ Returns true if this instance represents the totals for a club
            (rather than being specific to a particular CSHC team).
        """
        return self.team is None

    def reset(self):
        """Resets all stats to zero"""
        self.home_won = 0
        self.home_drawn = 0
        self.home_lost = 0
        self.home_gf = 0
        self.home_ga = 0
        self.away_won = 0
        self.away_drawn = 0
        self.away_lost = 0
        self.away_gf = 0
        self.away_ga = 0

    def add_match(self, match):
        """Adds a match to the stats"""
        assert match.final_scores_provided()
        assert match.opp_team.club_id == self.club_id
        assert (self.is_club_total()) or (match.our_team == self.team)

        if match.is_home:
            if match.was_won():
                self.home_won += 1
            elif match.was_drawn():
                self.home_drawn += 1
            else:
                assert match.was_lost()
                self.home_lost += 1
            self.home_gf += match.our_score
            self.home_ga += match.opp_score
        else:
            if match.was_won():
                self.away_won += 1
            elif match.was_drawn():
                self.away_drawn += 1
            else:
                assert match.was_lost()
                self.away_lost += 1
            self.away_gf += match.our_score
            self.away_ga += match.opp_score

    def accumulate_stats(self, stats):
        """Accumulate the given stats to the totals.
           Note: This should only be called for 'totals' stats.
        """
        assert self.is_club_total()
        self.home_won += stats.home_won
        self.home_drawn += stats.home_drawn
        self.home_lost += stats.home_lost
        self.home_gf += stats.home_gf
        self.home_ga += stats.home_ga
        self.away_won += stats.away_won
        self.away_drawn += stats.away_drawn
        self.away_lost += stats.away_lost
        self.away_gf += stats.away_gf
        self.away_ga += stats.away_ga
