import logging
from django.db import models
from django.db.models.query import QuerySet
from django.db import IntegrityError
from matches.models import Match
from members.models import Member
from competitions.models import Season

log = logging.getLogger(__name__)

 


class Award(models.Model):
    """ Abstract base class for all types of award """

    # A unique, user-friendly name for the award
    name = models.CharField("Award name", max_length=255, unique=True)

    class Meta:
        app_label = 'awards'
        abstract = True
        ordering = ['name']

    def __unicode__(self):
        return self.name


class MatchAwardQuerySet(models.Manager):
    """ Queries that relate to any Match Award Winners"""

    def MOM(self):
        award, created = self.get_or_create(name=MatchAward.MOM)
        return award

    def LOM(self):
        award, created = self.get_or_create(name=MatchAward.LOM)
        return award


class MatchAward(Award):
    """ An award that should be associated with a particular match"""

    objects = MatchAwardQuerySet()

    # Constants - these awards should always exist
    MOM = "Man of the Match"
    LOM = "Lemon of the Match"
    


class EndOfSeasonAward(Award):
    """ An award that is presented at the Annual Dinner"""
    pass
