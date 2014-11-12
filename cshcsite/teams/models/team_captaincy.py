import logging
from django.db import models
from members.models import Member
from club_team import ClubTeam
from core.models import first_or_none
from competitions.models import Season

log = logging.getLogger(__name__)


class TeamCaptaincy(models.Model):
    """Represents a member's term as captain of a team"""

    member = models.ForeignKey(Member)

    team  = models.ForeignKey(ClubTeam)

    is_vice = models.BooleanField("Vice-captain?", default=False, help_text="Check if this member is the vice captain (as opposed to the captain)")
    """True if this is a vice-captaincy role"""

    start = models.DateField("Start of captaincy", help_text="The date this member took over as captain")
    """The date that the member started their captaincy"""

    season = models.ForeignKey(Season, null=True, blank=True)

    class Meta:
        app_label = 'teams'
        verbose_name_plural = 'team captaincy'
        ordering = ['-start']

    def __unicode__(self):
        return unicode("{} {}: {}".format(self.team, self.role(), self.member))

    def role(self):
        """Returns a string representation of the player's role - either 'captain' or 'vice-captain'"""
        if(self.is_vice):
            return "vice-captain"
        return "captain"


    @staticmethod
    def get_captains(team, season):
        """Returns TeamCaptaincy objects corresponding to the captains for the specified team and season """
        return TeamCaptaincy.objects.filter(team=team, season=season, is_vice=False).order_by('-start')

    @staticmethod
    def get_vice_captains(team, season):
        """Returns TeamCaptaincy objects corresponding to the vice captains for the specified team and season """
        return TeamCaptaincy.objects.filter(team=team, season=season, is_vice=True).order_by('-start')
