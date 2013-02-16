from django.db import models
from datetime import datetime, date

class Season(models.Model):
    start = models.DateField()
    end = models.DateField()

    class Meta:
        app_label = 'club'

    def __unicode__(self):
        return "{}-{}".format(self.start, self.end)