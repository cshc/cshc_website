import logging
from django.db import models
from members.models import Member
from club_team import ClubTeam
from core.models import first_or_none

log = logging.getLogger(__name__)


class TeamCaptaincy(models.Model):
    """Represents a member's term as captain of a team"""

    member = models.ForeignKey(Member)

    team  = models.ForeignKey(ClubTeam)

    is_vice = models.BooleanField("Vice-captain?", default=False, help_text="Check if this member is the vice captain (as opposed to the captain)")
    """True if this is a vice-captaincy role"""

    start = models.DateField("Start of captaincy", help_text="The date this member took over as captain")
    """The date that the member started their captaincy"""

    class Meta:
        app_label = 'teams'
        verbose_name_plural = 'team captaincy'
        ordering = ['-start']

    def __unicode__(self):
        return "{} {}: {}".format(self.team, self.role(), self.member)

    def role(self):
        """Returns a string representation of the player's role - either 'captain' or 'vice-captain'"""
        if(self.is_vice):
            return "vice-captain"
        return "captain"


    @staticmethod
    def get_captain(team, season):
        """Returns a Member object corresponding to the captain for the specified team and season, or None if there was no captain"""
        return TeamCaptaincy._get_captain(team, season, False)

    @staticmethod
    def get_vice_captain(team, season):
        """Returns a Member object corresponding to the vice captain for the specified team and season, or None if there was no vice captain"""
        return TeamCaptaincy._get_captain(team, season, True)

    @staticmethod
    def _get_captain(team, season, is_vice):
        """Returns a Member object corresponding to the captain/vice-captain for the specified team and season, or None if there was no captaincy could be found"""
        try:
            captaincy = first_or_none(TeamCaptaincy.objects.filter(team=team, start__lte=season.end, is_vice=is_vice).order_by('-start'))
            if captaincy is not None:
                return captaincy.member
        except TeamCaptaincy.DoesNotExist:
            pass
        return None