from django.db import models
from league import League

class Cup(models.Model):
    name = models.CharField("Cup Name", max_length=255, unique=True, default=None)
    league = models.ForeignKey(League, null=True, on_delete=models.SET_NULL, help_text="The league, if any, that oversees this cup competition")

    class Meta:
        app_label = 'club'
        verbose_name = 'cup competition'

    def __unicode__(self):
        return self.name