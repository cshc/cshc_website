from django.db import models
from django.db import IntegrityError
from datetime import datetime, date

class Season(models.Model):
    start = models.DateField("Season start", help_text="(Approx) first day of the season")
    end = models.DateField("Season end", help_text="(Approx) last day of the season")

    class Meta:
        app_label = 'club'
        ordering = ['start']
        get_latest_by = "start"

    def __unicode__(self):
        return "{}-{}".format(self.start, self.end)

    def save(self, *args, **kwargs):
        # TODO: Prevent any overlapping seasons
        if (self.start >= self.end): 
            raise IntegrityError("The start of the season must be before the end of the season")
        
        super(Season, self).save(*args, **kwargs) 