""" The DivisionResult model represents a team's (CSHC or other)
    playing record in a particular season and division.

    This model is used to populate the league tables found on the
    club teams' pages.

    Note: The data from seasons prior to 2012-2013 has been imported
    from spreadsheets kept by Neil Sneade. The import script can be
    found at cshcsite/core/management/commands/import_league_tables.py
    and makes use of the league tables (in CSV format) found in
    cshcsite/import/league_tables.

    DivisionResult data for the current season is now updated as part
    of the nightly cronjob task by scraping the East League's website
    for data. THIS IS ERROR-PRONE DUE TO THE VOLATILE NATURE OF THE
    EXTERNAL WEBSITE'S LAYOUT ETC. If the nightly task reports errors
    in the scraping (e.g. 'Failed to parse league table'), you will have
    to debug the scraping code found in cshcsite/teams/league_scraper.py
    to work out what the problem is and implement a fix. In a perfect
    world, this league data would be available from the East League's
    website via a RESTful API. One can dream...

"""

from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManager


class DivisionResultQuerySet(QuerySet):
    """ Queries that relate to Division Results"""

    def league_table(self, division, season):
        """Returns all teams in the division in that season, ordered by position"""
        return self.filter(division=division, season=season).select_related('our_team', 'opp_team', 'division__club', 'season').order_by('position')


class DivisionResult(models.Model):
    """ Represents a team's (CSHC or other) playing record in
        a particular season and division.
    """

    # Only one of these fields should be populated, depending
    # on whether the team is a Cambridge South team or not.
    our_team = models.ForeignKey('teams.ClubTeam', null=True)
    opp_team = models.ForeignKey('opposition.Team', null=True)

    # Avoid circular reference issues by referring to the other
    # models using strings
    division = models.ForeignKey('competitions.Division')
    season = models.ForeignKey('competitions.Season')

    position = models.PositiveSmallIntegerField()
    played = models.PositiveSmallIntegerField(default=0)
    won = models.PositiveSmallIntegerField(default=0)
    drawn = models.PositiveSmallIntegerField(default=0)
    lost = models.PositiveSmallIntegerField(default=0)
    goals_for = models.PositiveSmallIntegerField(default=0)
    goals_against = models.PositiveSmallIntegerField(default=0)
    goal_difference = models.SmallIntegerField(default=0)
    points = models.PositiveSmallIntegerField(default=0)
    notes = models.TextField(blank=True,
                             help_text="E.g. C for champion, P for promoted, R for relegated")

    objects = PassThroughManager.for_queryset_class(DivisionResultQuerySet)()

    class Meta:
        """ Meta-info for the DivisionResult model."""
        app_label = 'competitions'
        unique_together = ('season', 'division', 'position')
        ordering = ('season', 'division', 'position')

    def clean(self):
        # our_team xor opp_team
        if self.our_team and self.opp_team:
            raise ValidationError("You cannot specify both our team and an opposition team ({})".format(self))
        if not self.our_team and not self.opp_team:
            raise ValidationError("You cannot specify neither our team nor an opposition team ({})".format(self))

        if (self.won + self.drawn + self.lost) != self.played:
            raise ValidationError("Won + Drawn + Lost not equal to Played ({})".format(self))

        if (self.goals_for - self.goals_against) != self.goal_difference:
            raise ValidationError("Goals For - Goals Against not equal to Goal Difference ({})".format(self))

    def __unicode__(self):
        return unicode("{} - {} ({})".format(self.team_name, self.division, self.season))


    @property
    def team_name(self):
        """ Gets the team name."""
        if self.opp_team:
            return self.opp_team.genderless_name()
        return self.our_team.genderless_abbr_name()

    @property
    def team(self):
        """ Gets the team (may be an instance of CSHC ClubTeam or opposition Team)"""
        return self.opp_team if self.opp_team else self.our_team

    @models.permalink
    def get_absolute_url(self):
        """ returns the url either for the CSHC team or the opposition team's club."""
        if self.opp_team:
            return self.opp_team.club.get_absolute_url()
        return self.our_team.get_absolute_url()
