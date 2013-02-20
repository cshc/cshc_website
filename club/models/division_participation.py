from django.db import models
from django.db import IntegrityError
from team import Team
from division_season import DivisionSeason

class DivisionParticipation(models.Model):
    team = models.ForeignKey(Team)
    div_season = models.ForeignKey(DivisionSeason, verbose_name="Division")
    final_pos = models.PositiveSmallIntegerField("Final position", null=True, blank=True, default=None, help_text="Once the season is complete, enter the final league position here")
    promoted = models.BooleanField(default=False, help_text="Check if the team was promoted at the end of the season")
    relegated = models.BooleanField(default=False, help_text="Check if the team was relegated at the end of the season")
    champions = models.BooleanField(default=False, help_text="Check if the team were division champions")

    class Meta:
        app_label = 'club'
        verbose_name_plural = 'division participation'
        unique_together = ('team', 'div_season')

    def __unicode__(self):
        return "{} - {}".format(self.team, self.div_season)

    def save(self, *args, **kwargs):
        if (self.promoted and self.relegated):
            raise IntegrityError("A team cannot be promoted AND relegated.")
        if(self.champions and (self.final_pos != 1)):
            raise IntegrityError("Final position must be 1 for division champions.")
        # Note - it is possible to be division champion and get relegated (for example if you're relegated
        #        for disciplinary reasons)
        #      - it is also possible to be champion and not be promoted (for example if you're in
        #        the top division)
        super(DivisionParticipation, self).save(*args, **kwargs) 