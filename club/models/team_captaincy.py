from django.db import models
from member import Member
from team import Team

class TeamCaptaincy(models.Model):
    member = models.ForeignKey(Member)
    team  = models.ForeignKey(Team)
    is_vice = models.BooleanField("Vice-captain?", default=False, help_text="Check if this member is the vice captain (as opposed to the captain)")
    start = models.DateField("Start of captaincy", help_text="The date this member took over as captain")

    class Meta:
        app_label = 'club'
        verbose_name_plural = 'team captaincy'
        ordering = ['-start']

    def __unicode__(self):
        return "{} {}: {}".format(self.team, self.role(), self.member)

    def role(self):
        if(self.is_vice):
            return "vice-captain"
        return "captain"
