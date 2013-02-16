from django.db import models
from season import Season
from division import Division

class DivisionSeason(models.Model):
    division = models.ForeignKey(Division, related_name="+")
    season = models.ForeignKey(Season, related_name="+")

    class Meta:
        app_label = 'club'
        # There can be only one division competition per season
        unique_together = ('division', 'season',) 

    def __unicode__(self):
        return "{} ({})".format(self.division, self.season)