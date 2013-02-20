from django.db import models

class League(models.Model):
    name = models.CharField("League Name", max_length=255, unique=True, default=None)
    url = models.URLField("League Website", null=True, blank=True, default=None, help_text="The club's website (if it has one)")

    class Meta:
        app_label = 'club'
        ordering = ['name']

    def __unicode__(self):
        return self.name

