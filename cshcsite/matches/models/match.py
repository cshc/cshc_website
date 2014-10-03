import logging
from django.db import models, IntegrityError
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from django.utils import timezone
from datetime import datetime, time
from model_utils import Choices, fields
from model_utils.managers import PassThroughManager
from core.models import splitify, not_none_or_empty
from teams.models import ClubTeam, ClubTeamSeasonParticipation
from opposition.models import Team
from members.models import Member
from venues.models import Venue
from competitions.models import Season, Division, Cup

log = logging.getLogger(__name__)


class MatchQuerySet(QuerySet):
    """ Queries that relate to Matches"""

    def fixtures(self):
        """Returns only matches in the future, ordered by date"""
        return self.filter(date__gte=datetime.now().date()).order_by('date', 'time')

    def results(self):
        """Returns only matches in the past, ordered by date"""
        return self.filter(date__lt=datetime.now().date()).order_by('date', 'time')

    def reports(self):
        """Returns only results with match reports"""
        return self.results().exclude(report_body__isnull=True).exclude(report_body='')

    def this_season(self):
        """Returns only this season's matches"""
        return self.by_season(Season.current())

    def by_season(self, season):
        """Returns only matches in the specified season"""
        return self.filter(season=season)

    def by_date(self, date):
        """Returns only matches on the specified date"""
        return self.filter(date=date).order_by('our_team__position')

    def by_report_author(self, member):
        """Returns only matches whose match report was written by the specified member"""
        return self.filter(report_author=member)


class Match(models.Model):
    """
    Represents a match.

    Note: both fixtures and results are classed as matches:
        Fixtures are just matches in the future
        Results are matches in the past
    """

    # Each match is either a home or away fixture
    HOME_AWAY = Choices('Home', 'Away')

    # If the match wasn't played, an alternative outcome should be entered
    ALTERNATIVE_OUTCOME = Choices('Postponed', 'Cancelled', 'Walkover', 'BYE')

    # We keep track of whether a match is a league, cup or just a friendly match
    FIXTURE_TYPE = Choices('Friendly', 'League', 'Cup')

    # Avoid magic numbers. However this simple constant definition is insufficient if these values ever change!
    POINTS_FOR_WIN = 3
    POINTS_FOR_DRAW = 1
    POINTS_FOR_LOSS = 0

    # Walk-over matches must be either 3-0 or 5-0 (depending on the league)
    WALKOVER_SCORE_W1 = 3
    WALKOVER_SCORE_W2 = 5
    WALKOVER_SCORE_L = 0

    # The Cambridge South team playing in this match
    our_team = models.ForeignKey(ClubTeam, verbose_name="Our team")

    # The opposition team
    opp_team = models.ForeignKey(Team, verbose_name="Opposition team")

    # The match venue
    venue = models.ForeignKey(Venue, null=True, blank=True, on_delete=models.SET_NULL)

    # Is the match a home or away fixture for South
    home_away = models.CharField("Home/Away", max_length=5, choices=HOME_AWAY, default=HOME_AWAY.Home)

    # The type of fixture
    fixture_type = models.CharField("Fixture type", max_length=10, choices=FIXTURE_TYPE, default=FIXTURE_TYPE.League)

    # The fixture date
    date = models.DateField("Fixture date")

    # The fixture start time. This can be left blank if its not known.
    time = models.TimeField("Start time", null=True, blank=True, default=None)

    # The alternative match outcome if it wasn't actually played
    alt_outcome = models.CharField("Alternative outcome", max_length=10, null=True, blank=True, default=None, choices=ALTERNATIVE_OUTCOME)

    # Cambridge South's final score
    our_score = models.PositiveSmallIntegerField("Our score", null=True, blank=True, default=None)

    # The opposition's final score
    opp_score = models.PositiveSmallIntegerField("Opposition's score", null=True, blank=True, default=None)

    # Cambridge South's half time score
    our_ht_score = models.PositiveSmallIntegerField("Our half-time score", null=True, blank=True, default=None)

    # The opposition's half time score
    opp_ht_score = models.PositiveSmallIntegerField("Opposition's half-time score", null=True, blank=True, default=None)

    # The total number of own goals scored by the opposition.
    # Note - Cambs South own goals are recored in the Appearance model (as we care about who scored the own goal!)
    opp_own_goals = models.PositiveSmallIntegerField("Opposition own-goals", default=0)

    # A short paragraph that can be used to hype up the match before its played - can be HTML
    # TODO: Prevent entering pre-match hype for matches in the past?
    pre_match_hype = fields.SplitField("Pre-match hype", blank=True)

    # The (optional) title of the match report
    report_title = models.CharField("Match report title", max_length=200, blank=True)

    # The (optional) match report author
    report_author = models.ForeignKey(Member, verbose_name="Match report author", null=True, blank=True, on_delete=models.SET_NULL, related_name="match_reports")

    # The actual match report text - can be HTML
    report_body = fields.SplitField("Match report", blank=True)

    # The datetime at which the report was first published
    report_pub_timestamp = models.DateTimeField("Match report publish timestamp", editable=False, default=None, null=True)

    # Advanced fields - typically leave as default value ######################

    # If True, this match should NOT count towards Goal King stats
    ignore_for_goal_king = models.BooleanField(default=False, help_text="Ignore this match when compiling Goal King stats")

    # If True, this match should NOT count towards Southerners League stats
    ignore_for_southerners = models.BooleanField(default=False, help_text="Ignore this match when compiling Southerners League stats")

    # Sometimes despite the clubs' kit clashing, we still play in our normal home kit. This can be recorded here.
    override_kit_clash = models.BooleanField(default=False, help_text="Ignore normal kit-clash with this club for this match")

    # Sometimes goals scored in shorter matches (e.g. in a tournament) will count a different amount towards the 'goals-per-game' stats
    gpg_pro_rata = models.FloatField(default=1.0, help_text="Goals-per-game multiplier. Only change this from the default value for matches of a different length.")

    # Derived attributes ######################################################
    # - these values cannot be entered in a form - they are derived based on the other attributes
    season = models.ForeignKey(Season, editable=False)
    division = models.ForeignKey(Division, null=True, blank=True, editable=False, on_delete=models.PROTECT)
    cup = models.ForeignKey(Cup, null=True, blank=True, editable=False, on_delete=models.PROTECT)

    # Convenience attribute listing all members who made an appearance in this match
    players = models.ManyToManyField(Member, through="Appearance", related_name="matches")

    objects = PassThroughManager.for_queryset_class(MatchQuerySet)()

    class Meta:
        app_label = 'matches'
        verbose_name_plural = "matches"
        ordering = ['date']

    def __unicode__(self):
        return unicode("{} vs {} ({}, {})".format(self.our_team, self.opp_team, self.fixture_type, self.date))

    @models.permalink
    def get_absolute_url(self):
        return ('match_detail', [self.pk])

    def clean(self):
        # If its a walkover, check the score is a valid walkover score
        if self.alt_outcome == Match.ALTERNATIVE_OUTCOME.Walkover and not Match.is_walkover_score(self.our_score, self.opp_score):
            raise ValidationError("A walk-over score must be 3-0, 5-0, 0-3 or 0-5. Score = {}-{}".format(self.our_score, self.opp_score))

        # If its cancelled or postponed or BYE, check the scores are not entered
        if((self.alt_outcome == Match.ALTERNATIVE_OUTCOME.Cancelled or
            self.alt_outcome == Match.ALTERNATIVE_OUTCOME.Postponed or
            self.alt_outcome == Match.ALTERNATIVE_OUTCOME.BYE) and
            (self.our_score != None or self.opp_score != None or self.our_ht_score != None or self.opp_ht_score != None)):
            raise ValidationError("A cancelled or postponed match should not have scores")

        if self.alt_outcome == None:
            # You can't specify one score without the other
            if((self.our_score != None and self.opp_score == None) or
               (self.our_score == None and self.opp_score != None)):
                raise ValidationError("Both scores must be provided")

            # ...same goes for half time scores
            if((self.our_ht_score != None and self.opp_ht_score == None) or
               (self.our_ht_score == None and self.opp_ht_score != None)):
                raise ValidationError("Both half-time scores must be provided")

            # The opposition can't score more own goals than our total score
            if(self.our_score != None and
               self.opp_own_goals > self.our_score):
                raise ValidationError("Too many opposition own goals")

            # Half-time scores must be <= the final scores
            if(self.all_scores_provided()):
                if(self.our_ht_score > self.our_score or
                   self.opp_ht_score > self.opp_score):
                    raise ValidationError("Half-time scores cannot be greater than final scores")

        # Automatically set the season based on the date
        try:
            self.season = Season.objects.by_date(self.date)
        except Season.DoesNotExist:
            raise ValidationError("This date appears to be outside of any recognised season.")

        if self.fixture_type == Match.FIXTURE_TYPE.League:
            # Automatically set the division based on the team and season
            try:
                self.division = ClubTeamSeasonParticipation.objects.get(team=self.our_team, season=self.season).division
            except Division.DoesNotExist:
                raise ValidationError("{} is not participating in a division in the season {}".format(self.our_team, self.season))
        else:
            self.division = None    # Clear the division field

        if self.fixture_type == Match.FIXTURE_TYPE.Cup:
            # Automatically set the cup based on the team and season
            try:
                self.cup = ClubTeamSeasonParticipation.objects.get(team=self.our_team, season=self.season).cup
            except Cup.DoesNotExist:
                raise ValidationError("{} is not participating in a cup in the season {}".format(self.our_team, self.season))
        else:
            self.cup = None    # Clear the cup field

    def save(self, *args, **kwargs):
        """ Set a few automatic fields and then save """
        # Automatically add a split in the match report and pre-match-hype
        self.report_body = splitify(self.report_body.content)
        self.pre_match_hype = splitify(self.pre_match_hype.content)

        # Timestamp the report publish datetime when its first created
        if self.report_pub_timestamp is None and not_none_or_empty(self.report_body.content):
            self.report_pub_timestamp = timezone.now()

        super(Match, self).save(*args, **kwargs)

    @property
    def is_home(self):
        """Returns True if this is a home fixture"""
        return self.home_away == Match.HOME_AWAY.Home

    def home_away_abbrev(self):
        """ Returns an abbreviated representation of the home/away status
        """
        if self.is_home:
            return 'H'
        else:
            return 'A'

    def kit_clash(self):
        """Returns true if there is a kit-clash for this fixture

            Note that this takes into account the override_kit_clash field.
            Home    Clash   Override    Return
            F       F       F           F
            F       F       T           T
            F       T       F           T
            F       T       T           F
            T       F       F           F
            T       F       T           T
            T       T       F           F
            T       T       T           T
        """
        if self.is_home:
            return self.override_kit_clash
        else:
            clash = self.opp_team.club.kit_clash(self.our_team.gender)
            return (clash and not self.override_kit_clash) or (not clash and self.override_kit_clash)

    def has_report(self):
        """Returns True if this match has a match report"""
        return self.report_body and not_none_or_empty(self.report_body.content)

    def datetime(self):
        """
        Convenience method to retrieve the date and time as one datetime object.
        Returns just the date if the time is not set.
        """
        if(self.time != None):
            return datetime.combine(self.date, self.time)
        return datetime.combine(self.date, time())

    def is_off(self):
        return self.alt_outcome in (Match.ALTERNATIVE_OUTCOME.Postponed, Match.ALTERNATIVE_OUTCOME.Cancelled)

    def is_in_past(self):
        """ Returns True if the match date/datetime is in the past."""
        if(self.time != None):
            return self.datetime() < datetime.now()
        return self.date < datetime.today().date()


    def time_display(self):
        """ Gets a formatted display of the match time.

            If the match time is not known, returns '???'
            if the match is in the past or 'TBD' if the match
            is in the future.
        """
        if self.time:
            return self.time.strftime('%H:%M')
        elif self.is_in_past():
            return '???'
        else:
            return 'TBD'

    def match_title_text(self):
        """
        Gets an appropriate match title regardless of the status of the match.
        Examples include:
            "Men's 1sts thrash St Neots"
            "M1 vs St Neots Men's 1sts"
            "M1 vs St Neots Men's 1sts - POSTPONED"
            "M1 vs St Neots Men's 1sts - CANCELLED"
            "M1 3-0 St Neots Men's 1sts (WALK-OVER)"
            "M1 5-1 St Neots Men's 1sts"
        """
        if not_none_or_empty(self.report_title):
            return self.report_title
        else:
            return self.fixture_title()

    def fixture_title(self):
        """
        Returns the title of this fixture in one of the following formats:
            Fixtures:- "M1 vs St Neots Men's 1sts"
            Results:-  "M1 3-0 St Neots Men's 1sts"
        """
        if self.alt_outcome == Match.ALTERNATIVE_OUTCOME.Walkover:
            return "{} {}-{} {} (WALK-OVER)".format(self.our_team, self.our_score, self.opp_score, self.opp_team)

        elif self.alt_outcome is not None:
            return "{} vs {} - {}".format(self.our_team, self.opp_team, self.get_alt_outcome_display())

        elif not self.final_scores_provided():
            return "{} vs {}".format(self.our_team, self.opp_team)

        else:
            return "{} {}-{} {}".format(self.our_team, self.our_score, self.opp_score, self.opp_team)

    @staticmethod
    def is_walkover_score(score1, score2):
        """
        Checks if the given scores are valid walk-over scores.
        Valid results are 3-0, 5-0, 0-3, 0-5.
        """
        if(score1 == Match.WALKOVER_SCORE_W1 or score1 == Match.WALKOVER_SCORE_W2):
            return score2 == Match.WALKOVER_SCORE_L
        elif(score2 == Match.WALKOVER_SCORE_W1 or score2 == Match.WALKOVER_SCORE_W2):
            return score1 == Match.WALKOVER_SCORE_L
        else:
            return False

    def ht_scores_provided(self):
        """ Returns true if both half-time scores are not None."""
        return (self.our_ht_score != None and
                self.opp_ht_score != None)

    def final_scores_provided(self):
        """ Returns true if both full-time/final scores are not None."""
        return (self.our_score != None and
                self.opp_score != None)

    def all_scores_provided(self):
        """ Returns true if both half-time and full-time scores are provided."""
        return self.final_scores_provided() and self.ht_scores_provided()

    def was_won(self):
        """ Returns true if our team won the match. """
        return (self.final_scores_provided() and
                self.our_score > self.opp_score)

    def was_lost(self):
        """ Returns true if our team lost the match. """
        return (self.final_scores_provided() and
                self.our_score < self.opp_score)

    def was_drawn(self):
        """ Returns true if the match was drawn. """
        return (self.final_scores_provided() and
                self.our_score == self.opp_score)

    def score_display(self):
        """
        Convenience method for displaying the score.
        Examples include:
        "3-2"         (normal result)
        ""            (blank - no result yet)
        "Cancelled"   (alt_outcome not None)
        """
        if self.alt_outcome is not None:
            return self.get_alt_outcome_display()
        if not self.final_scores_provided():
            return "-"
        return "{}-{}".format(self.our_score, self.opp_score)

    def simple_venue_name(self):
        """Returns 'Away' if this is not a home match. Otherwise returns the short_name attribute value."""
        if self.venue:
            if self.is_home:
                if self.venue.short_name is not None:
                    return self.venue.short_name
                else:
                    return self.venue.name
            return "Away"
        elif self.is_in_past():
            return '???'
        else:
            return 'TBD'

