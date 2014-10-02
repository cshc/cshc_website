import logging
from django.db import models
from django.db.models.query import QuerySet
from django.core.exceptions import ValidationError
from model_utils.managers import PassThroughManager
from competitions.models import Season
from core.models import TeamGender
from .member import Member

log = logging.getLogger(__name__)


class CommitteePosition(models.Model):
    """ Represents the name of a position on the committee.
    """

    name = models.CharField(max_length=100, default=None)

    gender = models.CharField("Mens/Ladies/Mixed", max_length=6, choices=TeamGender)

    index = models.PositiveSmallIntegerField("Index", help_text="Used for visual ordering of the committee", default=0)

    class Meta:
        app_label = 'members'
        unique_together = ('gender', 'index')
        # By default, list the general committee members first, then ladies then men.
        ordering = ('-gender', 'index')

    def __unicode__(self):
        if self.gender == TeamGender.Mixed:
            return unicode(self.name)
        else:
            return unicode("{} ({})".format(self.name, self.gender))


class CommitteeMembershipQuerySet(QuerySet):
    """ Queries that relate to Committee Membership"""

    def by_member(self, member):
        """Returns only committee membership for the specified member"""
        return self.filter(member=member)

    def by_position(self, position):
        """Returns only committee membership for the specified position"""
        return self.filter(position=position)

    def by_season(self, season):
        """Returns only committee membership for the specified season"""
        return self.filter(season=season).order_by('position__index')

    def current(self):
        """ Returns only current committee membership, if any."""
        return self.filter(season=Season.current()).order_by('position__index')


class CommitteeMembership(models.Model):
    """ This model represents membership of the club committee. A member
        may hold zero or more committee positions in a particular season.

        The actual positions may vary from season to season but are captured
        in the CommitteePosition model. If a new position is created, a new
        CommitteePosition entry should be added for it.
    """
    # The club member in the committee
    member = models.ForeignKey('Member')

    # The season in which the club member was on the committee
    season = models.ForeignKey('competitions.Season')

    # The committee position
    position = models.ForeignKey('CommitteePosition')

    objects = PassThroughManager.for_queryset_class(CommitteeMembershipQuerySet)()

    class Meta:
        app_label = 'members'
        ordering = ['member', 'position', 'season']
        # Only one person can hold a particular position in a particular season
        unique_together = ('position', 'season')

    def __unicode__(self):
        return unicode("{} - {} ({})".format(self.member, self.position, self.season))

