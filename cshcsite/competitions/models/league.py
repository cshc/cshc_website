""" The League model represents a single hockey league,
    which can be made up of multiple divisions.
"""

from django.db import models


class League(models.Model):
    """Represents a hockey league"""

    # The (unique) name of the league
    name = models.CharField("League Name", max_length=255, unique=True, default=None)

    # The (external) league website - optional
    url = models.URLField("League Website", blank=True,
                          help_text="The club's website (if it has one)")

    class Meta:
        """ Meta-info for the League model."""
        app_label = 'competitions'
        ordering = ['name']

    def __unicode__(self):
        return unicode(self.name)

