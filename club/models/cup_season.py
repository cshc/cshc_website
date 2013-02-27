from django.db import models
from season import Season
from cup import Cup

class CupSeason(models.Model):
    cup = models.ForeignKey(Cup, related_name="cup_seasons")
    season = models.ForeignKey(Season, related_name="cup_seasons")

    class Meta:
        app_label = 'club'
        # There can be only one cup competition per season
        unique_together = ('cup', 'season',) 

    def __unicode__(self):
        return "{} ({})".format(self.cup, self.season)