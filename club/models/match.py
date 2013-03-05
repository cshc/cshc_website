from django.db import models
from django.db import IntegrityError
from django.core.urlresolvers import reverse
from datetime import datetime, date, time
from team import Team
from venue import Venue
from division_season import DivisionSeason
from cup_season import CupSeason
from season import Season
from choices import HomeAway, AlternativeOutcome, FixtureType, CupRound

class Match(models.Model):

    # Walk-over matches must be either 3-0 or 5-0 (depending on the league)
    WALKOVER_SCORE_W1 = 3
    WALKOVER_SCORE_W2 = 5
    WALKOVER_SCORE_L = 0
    
    our_team = models.ForeignKey(Team, verbose_name="Our team", related_name="our_matches")
    opp_team = models.ForeignKey(Team, verbose_name="Opposition team", related_name="opp_matches")
    venue = models.ForeignKey(Venue, null=True, blank=True, on_delete=models.SET_NULL)
    home_away = models.CharField("Home/Away", max_length=1, choices=HomeAway.CHOICES, default=HomeAway.HOME)
    date = models.DateField("Fixture date")
    time = models.TimeField("Start time", null=True, blank=True, default=None)
    alt_outcome = models.CharField("Alternative outcome", max_length=2, default=AlternativeOutcome.NONE, choices=AlternativeOutcome.CHOICES)
    our_score = models.PositiveSmallIntegerField("Our score", null=True, blank=True, default=None)
    opp_score = models.PositiveSmallIntegerField("Opposition's score", null=True, blank=True, default=None)
    our_ht_score = models.PositiveSmallIntegerField("Our half-time score", null=True, blank=True, default=None)
    opp_ht_score = models.PositiveSmallIntegerField("Opposition's half-time score", null=True, blank=True, default=None)
    opp_own_goals = models.PositiveSmallIntegerField("Opposition own-goals", default=0)
    report_title = models.CharField("Match report title", max_length=200, null=True, blank=True, default=None)
    report_author = models.CharField("Match report author", max_length=200, null=True, blank=True, default=None)
    report_body = models.TextField("Match report", null=True, blank=True, default=None)

    class Meta:
        app_label = 'club'
        verbose_name_plural = "matches"
        ordering = ['date']

    def __unicode__(self):
        return "{} vs {} ({}, {})".format(self.our_team, self.opp_team, self.fixture_type, self.date)

    def get_absolute_url(self):
        return reverse('club.views.matches.details', args=[self.pk])

    def save(self, *args, **kwargs):
        """ Validate the match details and then save """
        if(self.our_team == self.opp_team):
            raise IntegrityError("A team cannot play themselves in a match")
            
        if (self.alt_outcome == AlternativeOutcome.WALKOVER and not Match.is_walkover_score(self.our_score, self.opp_score)):
            raise IntegrityError("A walk-over score must be {}".format(Match.valid_walkover_scores()))
            
        if((self.alt_outcome == AlternativeOutcome.CANCELLED or self.alt_outcome == AlternativeOutcome.POSTPONED) and
            (self.our_score != None or self.opp_score != None or self.our_ht_score != None or self.opp_ht_score != None)):
            raise IntegrityError("A cancelled or postponed match should not have scores")
            
        if(self.alt_outcome == AlternativeOutcome.NONE):
            if((self.our_score != None and self.opp_score == None) or
               (self.our_score == None and self.opp_score != None)):
                raise IntegrityError("Both scores must be provided")
            
            if(self.our_score != None and 
               self.opp_own_goals > self.our_score):
                raise IntegrityError("Too many opposition own goals")
            
            if(self.all_scores_provided()):
                if(self.our_ht_score > self.our_score or 
                   self.opp_ht_score > self.opp_score):
                    raise IntegrityError("Half-time scores cannot be greater than final scores")
               
        super(Match, self).save(*args, **kwargs) 
        
    # Overridden in derived classes
    @property
    def fixture_type(self):
        return FixtureType.Friendly_display
        
    def has_result(self):
        return self.report_body != None

    def has_team(self):
        return self.players.count() > 0

    def datetime(self):
        """ 
        Convenience method to retrieve the date and time as one datetime object.
        Returns just the date if the time is not set.
        """
        if(self.time != None):
            return datetime.combine(self.date, self.time)
        return self.date
    
    def is_in_past(self):
        """ Returns true if the match date/datetime is in the past."""
        if(self.time != None):
            return self.datetime() < datetime.now()
        return self.date < datetime.today().date()
        
    def match_title_text(self):
        """ 
        Gets an appropriate match title regardless of the status of the match.
        Examples include:
            "Men's 1sts thrash St Neots"
            "Cambridge South Men's 1sts vs St Neots Men's 1sts"
            "Cambridge South Men's 1sts vs St Neots Men's 1sts - POSTPONED"
            "Cambridge South Men's 1sts vs St Neots Men's 1sts - CANCELLED"
            "Cambridge South Men's 1sts 3-0 St Neots Men's 1sts (WALK-OVER)"
            "Cambridge South Men's 1sts 5-1 St Neots Men's 1sts"
        """
        if(self.report_title != None):
            return self.report_title
            
        elif(self.alt_outcome == AlternativeOutcome.WALKOVER):
            return "{} {}-{} {} (WALK-OVER)".format(self.our_team, self.our_score, self.opp_score, self.opp_team)
                
        elif(self.alt_outcome == AlternativeOutcome.POSTPONED):
            return "{} vs {} - POSTPONED".format(self.our_team, self.opp_team)
            
        elif(self.alt_outcome == AlternativeOutcome.CANCELLED):
            return "{} vs {} - CANCELLED".format(self.our_team, self.opp_team)
            
        elif(not self.final_scores_provided()):
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
    
    @staticmethod
    def valid_walkover_scores():
        return "{0}-{2}, {1}-{2}, {2}-{0} or {2}-{1}".format(Match.WALKOVER_SCORE_W1, Match.WALKOVER_SCORE_W2, Match.WALKOVER_SCORE_L)
    
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
        if(self.alt_outcome != AlternativeOutcome.NONE):
            return self.get_alt_outcome_display()
        if(not self.final_scores_provided(self)):
            return ""
        return "{}-{}".format(self.our_score, self.opp_score)


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