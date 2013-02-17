from django.db import models
from player import Player
from team import Team

class TeamCaptaincy(models.Model):
    player = models.ForeignKey(Player)
    team  = models.ForeignKey(Team)
    is_vice = models.BooleanField("Vice-captain?", default=False)
    start = models.DateField("Start of captaincy", auto_now_add=True, help_text="The date this player took over as captain")

    class Meta:
        app_label = 'club'
        verbose_name_plural = 'team captaincy'

    def __unicode__(self):
        return "{} {}: {}".format(self.team, self.role(), self.player)

    def role(self):
        if(self.is_vice):
            return "vice-captain"
        return "captain"