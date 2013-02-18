from django.db import models
from team import Team
from division_season import DivisionSeason

class DivisionParticipation(models.Model):
    team = models.ForeignKey(Team)
    div_season = models.ForeignKey(DivisionSeason, verbose_name="Division")
    final_pos = models.PositiveSmallIntegerField("Final position", null=True, blank=True, default=None, help_text="Once the season is complete, enter the final league position here")

    class Meta:
        app_label = 'club'
        verbose_name_plural = 'division participation'
        unique_together = ('team', 'div_season')

    def __unicode__(self):
        return "{} - {}".format(self.team, self.div_season)