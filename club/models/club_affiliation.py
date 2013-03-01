from django.db import models
from django.db import IntegrityError
from member import Member
from club import Club

class ClubAffiliation(models.Model):
    member = models.ForeignKey(Member)
    club = models.ForeignKey(Club)
    start = models.DateField("Date joined")
    end = models.DateField("Date left", null=True, blank=True, default=None)

    class Meta:
        app_label = 'club'
        ordering = ['member', 'start', 'club']

    def __unicode__(self):
        return "{} - {}".format(self.member, self.club)

    def save(self, *args, **kwargs):
        # Note that this does not check for larger 'circular promotion/relegation references'
        if (self.end != None and self.start >= self.end): 
            raise IntegrityError("The date this member joined the club cannot be after the date they left!")
        
        super(ClubAffiliation, self).save(*args, **kwargs) 
