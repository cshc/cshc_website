import logging
from django.db import models
from core.models import TeamGender
from league import League

log = logging.getLogger(__name__)


class Division(models.Model):
    """Represents a division within a league"""

    # Name of the division. Must be unique within a league.
    name = models.CharField("Division Name", max_length=255, default=None)

    # The league which runs this division
    league = models.ForeignKey(League, related_name="divisions", help_text="The league that is responsible for this division")

    # Denotes whether this is a mens, ladies or mixed league
    gender = models.CharField("Division gender (mens/ladies)", max_length=6, choices=TeamGender)

    class Meta:
        app_label = 'competitions'
        # A division's name must be unique within a league.
        # However two different leagues can have divisions with the same name
        unique_together = ('name', 'league', 'gender')
        ordering = ['league', 'gender', 'name']

    def __unicode__(self):
        return unicode("{} {}".format(self.league.name, self.name))
