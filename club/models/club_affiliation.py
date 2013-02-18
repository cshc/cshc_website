from django.db import models
from django.db import IntegrityError
from player import Player
from club import Club

class ClubAffiliation(models.Model):
    player = models.ForeignKey(Player)
    club = models.ForeignKey(Club)
    start = models.DateField("Date joined")
    end = models.DateField("Date left", null=True, blank=True, default=None)

    class Meta:
        app_label = 'club'

    def __unicode__(self):
        return "{} - {}".format(self.player, self.club)

    def save(self, *args, **kwargs):
        # Note that this does not check for larger 'circular promotion/relegation references'
        if (self.end != None and self.start >= self.end): 
            raise IntegrityError("The date this player joined the club cannot be after the date they left!")
        
        super(ClubAffiliation, self).save(*args, **kwargs) 