from django.db import models
from choices import TeamGender, TeamOrdinal
from club import Club

class Team(models.Model):
    club = models.ForeignKey(Club)
    gender = models.CharField("Team gender (mens/ladies)", max_length=2, choices=TeamGender.CHOICES)
    ordinal = models.CharField("Ordinal (1sts, 2nds etc)", max_length=2, choices=TeamOrdinal.CHOICES)   

    class Meta:
        app_label = 'club'
        # Within a club there can be only one team for a particular gender and ordinal combination
        unique_together = ('club', 'gender', 'ordinal')   

    def __unicode__(self):
        return "{} {}".format(self.club.name, self.name())

    def name(self):
        return "{} {}".format(self.get_gender_display(), self.get_ordinal_display())