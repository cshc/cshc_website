import logging
from django.db import models, IntegrityError
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManager

log = logging.getLogger(__name__)


class DivisionResultQuerySet(QuerySet):
    """ Queries that relate to Division Results"""

    def league_table(self, division, season):
        """Returns all teams in the division in that season, ordered by position"""
        return self.filter(division=division, season=season).select_related('our_team', 'opp_team', 'division__club', 'season').order_by('position')


class DivisionResult(models.Model):

    our_team = models.ForeignKey('teams.ClubTeam', null=True)
    opp_team = models.ForeignKey('opposition.Team', null=True)

    division = models.ForeignKey('competitions.Division')
    season = models.ForeignKey('competitions.Season')

    position = models.PositiveSmallIntegerField()
    played = models.PositiveSmallIntegerField(default=0)
    won = models.PositiveSmallIntegerField(default=0)
    drawn = models.PositiveSmallIntegerField(default=0)
    lost = models.PositiveSmallIntegerField(default=0)
    goals_for = models.PositiveSmallIntegerField(default=0)
    goals_against = models.PositiveSmallIntegerField(default=0)
    goal_difference = models.PositiveSmallIntegerField(default=0)
    points = models.PositiveSmallIntegerField(default=0)
    notes = models.TextField(blank=True, help_text="E.g. C for champion, P for promoted, R for relegated")

    objects = PassThroughManager.for_queryset_class(DivisionResultQuerySet)()

    class Meta:
        app_label = 'competitions'
        unique_together = ('season', 'division', 'position')
        ordering = ('season', 'division', 'position')

    def save(self, *args, **kwargs):
        # our_team xor opp_team
        if self.our_team and self.opp_team:
            raise IntegrityError("You cannot specify both our team and an opposition team ({})".format(self))
        if not self.our_team and not self.opp_team:
            raise IntegrityError("You cannot specify neither our team nor an opposition team ({})".format(self))

        if (self.won + self.drawn + self.lost) != self.played:
            raise IntegrityError("Won + Drawn + Lost not equal to Played ({})".format(self))

        if (self.goals_for - self.goals_against) != self.goal_difference:
            raise IntegrityError("Goals For - Goals Against not equal to Goal Difference ({})".format(self))

        super(DivisionResult, self).save(*args, **kwargs)

    def __unicode__(self):
        return "{} - {} ({})".format(self.team_name, self.division, self.season)


    @property
    def team_name(self):
        return "{}".format(self.opp_team if self.opp_team else self.our_team.abbr_name())

    @property
    def team(self):
        return self.opp_team if self.opp_team else self.our_team

    @models.permalink
    def get_absolute_url(self):
        return self.opp_team.club.get_absolute_url() if self.opp_team else self.our_team.get_absolute_url()
