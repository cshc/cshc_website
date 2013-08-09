import logging
from django.db import models
from django.db.models.query import QuerySet
from django.db import IntegrityError
from model_utils import Choices
from model_utils.managers import PassThroughManager
from core.models import not_none_or_empty
from competitions.models import Season, Division, Cup
from club_team import ClubTeam

log = logging.getLogger(__name__)


class ClubTeamSeasonParticipationQuerySet(QuerySet):
    """QuerySet for the ClubTeamSeasonParticipation model"""

    def current(self):
        """Returns just the participations for the current season"""
        return self.filter(season=Season.current())

    def by_season(self, season):
        """Returns just the participations for the specified season"""
        return self.filter(season=season)

    def by_team(self, team):
        """Returns just the participations for the specified team"""
        return self.filter(team=team)


class ClubTeamSeasonParticipation(models.Model):
    """Represents the participation of a Cambridge South team in a particular season.

       Includes division and cup participation.
    """

    DIVISION_RESULT = Choices('Promoted', 'Relegated', 'Champions')

    team = models.ForeignKey(ClubTeam)
    """The Cambridge South team participating in the division"""

    season = models.ForeignKey(Season)
    """The season in which the team participated in the division"""

    # Division ################################################################

    division = models.ForeignKey(Division, null=True)
    """The division in which the team participated in, if any."""

    team_photo = models.ImageField(upload_to='uploads/team_photos', null=True, blank=True)
    """A team photo (if available) from this sesason"""

    team_photo_caption = models.TextField(blank=True)
    """Caption for the team photo. Could include a list of who's who."""

    final_pos = models.PositiveSmallIntegerField("Final position", null=True, blank=True, default=None, help_text="Once the season is complete, enter the final league position here")
    """The final league position of the team"""

    division_result = models.CharField(max_length=20, choices=DIVISION_RESULT, null=True, blank=True, default=None, help_text="Set to one of the options if the team was promoted or relegated this season.")
    """Indicates if the team was promoted or relegated this season"""

    # The (external) URL of the division leauge table
    division_tables_url = models.URLField("League table website", blank=True)

    # The (external) URL of the division fixtures list
    division_fixtures_url = models.URLField("Fixtures website", blank=True)

    # Cup #####################################################################

    cup = models.ForeignKey(Cup, null=True, blank=True)
    """The cup the team participated in, if any."""

    cup_result = models.CharField("Cup result", max_length=100, null=True, blank=True, default=None, help_text="Where did the team get to in the cup? (Enter once cup participation is complete)")
    """How the team got on in the cup"""

    blurb = models.TextField(blank=True)
    """Some optional comments about the team this season."""

    objects = PassThroughManager.for_queryset_class(ClubTeamSeasonParticipationQuerySet)()


    class Meta:
        app_label = 'teams'
        # A team can only participate once per season!
        unique_together = ('team', 'season')

    def __unicode__(self):
        return "{} - {}".format(self.team, self.season)

    def save(self, *args, **kwargs):
        # Sanity checks
        if not self.division and not_none_or_empty(self.division_result):
            raise IntegrityError("Division result cannot be set if no division is selected.")

        if not self.division and self.final_pos is not None:
            raise IntegrityError("Final position cannot be set if no division is selected.")

        if not self.cup and not_none_or_empty(self.cup_result):
            raise IntegrityError("Cup result cannot be set if no cup is selected.")

        # Make sure the division gender matches the team gender!
        if self.division is not None and (self.team.gender != self.division.gender):
            raise IntegrityError("{} is a {} team but {} is a {} division", self.team, self.team.get_gender_display(), self.division, self.division.get_gender_display());

        # Make sure the cup gender matches the team gender!
        if self.cup is not None and (self.team.gender != self.cup.gender):
            raise IntegrityError("{} is a {} team but {} is a {} cup", self.team, self.team.get_gender_display(), self.cup, self.cup.get_gender_display());

        super(ClubTeamSeasonParticipation, self).save(*args, **kwargs)

