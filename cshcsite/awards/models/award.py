""" These models define the various awards that can be won
    in the club, both for a particular match and at the end
    of a season.
"""

from django.db import models

class Award(models.Model):
    """ Abstract base class for all types of award """

    # A unique, user-friendly name for the award
    name = models.CharField("Award name", max_length=255, unique=True)

    class Meta:
        """ Meta-info for the Award model."""
        app_label = 'awards'
        abstract = True
        ordering = ['name']

    def __unicode__(self):
        return unicode(self.name)


class MatchAwardQuerySet(models.Manager):
    """ Queries that relate to any Match Award Winners"""

    def mom(self):
        """ Returns the Man of the Match award, creating it
            if it doesn't already exist.
        """
        award, _ = self.get_or_create(name=MatchAward.MOM)
        return award

    def lom(self):
        """ Returns the Lemon of the Match award, creating it
            if it doesn't already exist.
        """
        award, _ = self.get_or_create(name=MatchAward.LOM)
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
