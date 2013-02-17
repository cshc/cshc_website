from django.db import models
from player import Player
from match import Match

class Appearance(models.Model):
    player = models.ForeignKey(Player)
    match = models.ForeignKey(Match)
    goals = models.PositiveSmallIntegerField("Goals scored", default=0)
    own_goals = models.PositiveSmallIntegerField("Own-goals scored", default=0)

    class Meta:
        app_label = 'club'

    def __unicode__(self):
        return "{} - {}".format(self.player, self.match)