from django.db import models
from member import Member
from match import Match

class Appearance(models.Model):
    member = models.ForeignKey(Member)
    match = models.ForeignKey(Match)
    goals = models.PositiveSmallIntegerField("Goals scored", default=0)
    own_goals = models.PositiveSmallIntegerField("Own-goals scored", default=0)
    green_card = models.BooleanField(default=False, help_text="Did the player receive a green card in the match?")
    yellow_card = models.BooleanField(default=False, help_text="Did the player receive a yellow card in the match?")
    red_card = models.BooleanField(default=False, help_text="Did the player receive a red card in the match?")

    class Meta:
        app_label = 'club'
        unique_together = ('member', 'match')  
        ordering = ['match', 'member']

    def __unicode__(self):
        return "{} - {}".format(self.member, self.match)
