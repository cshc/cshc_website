from django.db import models
from choices import TEAM_GENDER, ORDINAL
from club import Club

class Team(models.Model):
    club = models.ForeignKey(Club)
    gender = models.CharField("Team gender (mens/ladies)", max_length=2, choices=TEAM_GENDER)
    ordinal = models.CharField("Ordinal (1sts, 2nds etc)", max_length=2, choices=ORDINAL)   

    class Meta:
        app_label = 'club'

    def __unicode__(self):
        return "{} {}".format(self.club.name, self.name())

    def name(self):
        return "{} {}".format(self.get_gender_display(), self.get_ordinal_display())