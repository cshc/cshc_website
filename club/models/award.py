from django.db import models
from django.db import IntegrityError
from match import Match
from player import Player
from season import Season
from choices import AwardType

class Award(models.Model):
    name = models.CharField("Award name", max_length=255, unique=True)

    class Meta:
        app_label = 'club'
        abstract = True
        ordering = ['name']

    def __unicode__(self):
        return self.name

class MatchAward(Award):
    
    def __unicode__(self):
        return self.name

class EndOfSeasonAward(Award):
    
    def __unicode__(self):
        return self.name

class AwardWinner(models.Model):
    player = models.ForeignKey(Player, null=True, blank=True, default=None, help_text="(Leave blank if award winner is not a player)")
    awardee = models.CharField("Award winner", max_length=255, null=True, blank=True, default=None, help_text="Only use this field if the award winner is not a player")
    comment = models.TextField(help_text="Enter a short description of why this person received this award")

    class Meta:
        app_label = 'club'
        abstract = True

    def save(self, *args, **kwargs):
        if (self.player == None and 
            self.awardee == None):
            raise IntegrityError("You must specify either a player or an awardee (if the awardee is not a player)")
        
        super(AwardWinner, self).save(*args, **kwargs) 

    def awardee_name(self):
        if(self.player == None):
            return self.awardee
        return self.player

class MatchAwardWinner(AwardWinner):
    match = models.ForeignKey(Match)
    award = models.ForeignKey(MatchAward)
    
    def __unicode__(self):
        return "{} - {} ({})".format(self.award, self.awardee_name(), self.match)


class EndOfSeasonAwardWinner(AwardWinner):
    season = models.ForeignKey(Season)
    award = models.ForeignKey(EndOfSeasonAward)
    
    def __unicode__(self):
        return "{} - {} ({})".format(self.award, self.awardee_name(), self.season)