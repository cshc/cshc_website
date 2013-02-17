from django.db import models
from cup_season import CupSeason
from team import Team
from choices import CupResult

class CupParticipation(models.Model):
    team = models.ForeignKey(Team)
    cup_season = models.ForeignKey(CupSeason, verbose_name="Cup")
    result = models.CharField("Cup result", max_length=3, choices=CupResult.CHOICES, null=True, blank=True, default=None, help_text="Where did the team get to in the cup? (Enter once cup participation is complete)")

    class Meta:
        app_label = 'club'
        verbose_name_plural = 'cup participation'

    def __unicode__(self):
        return "{} - {}".format(self.team, self.cup_season)