from django.db import models
from team import Team
from venue import Venue
from division_season import DivisionSeason
from cup_season import CupSeason
from season import Season
from choices import HomeAway, MatchOutcome, FixtureType, CupRound

class Match(models.Model):
    our_team = models.ForeignKey(Team, verbose_name="Our team", related_name="+")
    opp_team = models.ForeignKey(Team, verbose_name="Opposition team", related_name="+")
    venue = models.ForeignKey(Venue, null=True, on_delete=models.SET_NULL)
    home_away = models.CharField("Home/Away", max_length=1, choices=HomeAway.CHOICES)
    date = models.DateField("Fixture date")
    time = models.TimeField("Start time", null=True, blank=True, default=None)
    outcome = models.CharField("Match outcome", max_length=2, default=MatchOutcome.PENDING, choices=MatchOutcome.CHOICES)
    our_score = models.PositiveSmallIntegerField("Our score", null=True, blank=True, default=None)
    opp_score = models.PositiveSmallIntegerField("Opposition's score", null=True, blank=True, default=None)
    our_ht_score = models.PositiveSmallIntegerField("Our half-time score", null=True, blank=True, default=None)
    opp_ht_score = models.PositiveSmallIntegerField("Opposition's half-time score", null=True, blank=True, default=None)
    opp_own_goals = models.PositiveSmallIntegerField("Opposition own-goals", default=0)
    report_title = models.CharField("Match report title", max_length=200, null=True, blank=True, default=None)
    report_body = models.TextField("Match report", null=True, blank=True, default=None)

    class Meta:
        app_label = 'club'
        verbose_name_plural = "matches"
        ordering = ['date']

    def __unicode__(self):
        return "{} vs {} ({}, {})".format(self.our_team, self.opp_team, self.fixture_type, self.date)

    @property
    def fixture_type(self):
        return FixtureType.Friendly_display

class DivisionMatch(Match):
    div_season = models.ForeignKey(DivisionSeason, verbose_name="Division")

    class Meta:
        app_label = 'club'
        verbose_name_plural = "division matches"

    @property
    def fixture_type(self):
        return FixtureType.League_display
    
class CupMatch(Match):
    cup_season = models.ForeignKey(CupSeason, verbose_name="Cup")
    round = models.CharField("Cup Round", max_length=2, choices=CupRound.CHOICES, default=CupRound.ROUND_1)

    class Meta:
        app_label = 'club'
        verbose_name_plural = "cup matches"
        # Note: cup_season and round should not be marked unique_together as there could be
        # replayed matches

    @property
    def fixture_type(self):
        return FixtureType.Cup_display

class FriendlyMatch(Match):
    season = models.ForeignKey(Season)

    class Meta:
        app_label = 'club'
        verbose_name_plural = "friendly matches"

    @property
    def fixture_type(self):
        return FixtureType.Friendly_display