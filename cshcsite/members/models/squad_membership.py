import logging
from django.db import models
from django.db.models.query import QuerySet
from django.core.exceptions import ValidationError
from model_utils.managers import PassThroughManager
from competitions.models import Season
from teams.models import ClubTeam
from .member import Member

log = logging.getLogger(__name__)


def validate_squad(team_id):
    try:
        t = ClubTeam.objects.get(pk=team_id)
        if t.short_name.lower() in ('mixed', 'indoor', 'vets'):
            raise ValidationError("Squad assignments must be to one of the Men's or Ladies teams")
    except ClubTeam.DoesNotExist:
        raise ValidationError("Team not found")


class SquadMembershipQuerySet(QuerySet):
    """ Queries that relate to Squad Membership"""

    def by_member(self, member):
        """Returns only squad membership for the specified member"""
        return self.filter(member=member)

    def by_team(self, team):
        """Returns only squad membership for the specified team"""
        return self.filter(team=team)

    def by_season(self, season):
        """Returns only squad membership for the specified season"""
        return self.filter(season=season)

    def current(self):
        """ Returns only current squad membership, if any."""
        return self.filter(season=Season.current())


class SquadMembership(models.Model):
    """ A player is nominally assigned to a squad each season. This models
        maintains info on squad membership over the years.
    """
    # The club member in a squad
    member = models.ForeignKey('Member')

    # The team (squad) which the club member was a part of
    team = models.ForeignKey('teams.ClubTeam', validators=[validate_squad])

    # The season in which the club member was in the team
    season = models.ForeignKey('competitions.Season')

    objects = PassThroughManager.for_queryset_class(SquadMembershipQuerySet)()

    class Meta:
        app_label = 'members'
        ordering = ['member', 'season']
        # A member can only be in one squad in a particular season
        unique_together = ('member', 'team', 'season')

    def __unicode__(self):
        return unicode("{} - {} ({})".format(self.member, self.team, self.season))

