from django.db import models

class League(models.Model):
    name = models.CharField("League Name", max_length=255, unique=True)

    class Meta:
        app_label = 'club'

    def __unicode__(self):
        return self.name

