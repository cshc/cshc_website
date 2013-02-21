from django.db import models
from choices import TeamGender, TeamOrdinal
from club import Club

class TeamManager(models.Manager):
        
    def mens(self):
        return self.get_query_set().filter(gender=TeamGender.MENS)
        
    def ladies(self):
        return self.get_query_set().filter(gender=TeamGender.LADIES)
        
    def mixed(self):
        return self.get_query_set().filter(gender=TeamGender.MIXED)
        
class OurTeamManager(TeamManager):
    def get_query_set(self):
        return super(OurTeamManager, self).get_query_set().filter(club = Club.our_club())
        
        
class OppositionTeamManager(TeamManager):
    def get_query_set(self):
        return super(OppositionTeamManager, self).get_query_set().exclude(club = Club.our_club())
    
        
class Team(models.Model):
    club = models.ForeignKey(Club)
    gender = models.CharField("Team gender (mens/ladies)", max_length=2, choices=TeamGender.CHOICES)
    ordinal = models.CharField("Ordinal (1sts, 2nds etc)", max_length=2, choices=TeamOrdinal.CHOICES)   

    # MANAGERS
    objects = models.Manager()          # The default manager.
    our_teams = OurTeamManager()        # Manages our teams.
    opp_teams = OppositionTeamManager() # Manages opposition teams
    
    class Meta:
        app_label = 'club'
        # Within a club there can be only one team for a particular gender and ordinal combination
        unique_together = ('club', 'gender', 'ordinal')   
        ordering = ['club', 'gender', 'ordinal']

    def __unicode__(self):
        return "{} {}".format(self.club.name, self.name())

    def name(self):
        return "{} {}".format(self.get_gender_display(), self.get_ordinal_display())
        
