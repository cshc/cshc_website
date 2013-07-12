import logging
from django.db import models

log = logging.getLogger(__name__)


class League(models.Model):
    """Represents a hockey league"""

    # The (unique) name of the league
    name = models.CharField("League Name", max_length=255, unique=True, default=None)

    # The (external) league website
    url = models.URLField("League Website", blank=True, help_text="The club's website (if it has one)")

    class Meta:
        app_label = 'competitions'
        ordering = ['name']

    def __unicode__(self):
        return self.name

