import logging
from django.db import models
from core.models import TeamGender
from league import League

log = logging.getLogger(__name__)


class Cup(models.Model):
    """Represents a Cup Competition"""

    # The (unique) name of the cup competition
    name = models.CharField("Cup Name", max_length=255, unique=True, default=None)

    # The league (if any) that oversees this cup competition
    league = models.ForeignKey(League, null=True, blank=True, on_delete=models.SET_NULL, help_text="The league, if any, that oversees this cup competition")

    # Defines if this cup is a men, ladies or mixed tournament
    gender = models.CharField("Mens/Ladies", max_length=6, choices=TeamGender)

    class Meta:
        app_label = 'competitions'
        verbose_name = 'cup competition'
        ordering = ['name']

    def __unicode__(self):
        return self.name