import logging
from django.db import models
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManager
from members.models import Member
from match import Match
from core.stats import MatchStats
from awards.models import MatchAwardWinner

log = logging.getLogger(__name__)


class AppearanceQuerySet(QuerySet):
    """Queries that relate to an appearance"""

    def by_member(self, member):
        """Returns only the appearances for a specific member"""
        return self.filter(member=member)

    def by_season(self, season):
        """Returns only the appearances for a particular season"""
        return self.select_related('match__season').filter(match__season=season)


class Appearance(models.Model):
    """
    Represents an appearance by a member in a match.
    This model also holds information on goals scored (incl own goals), and cards received.
    """
    # The person making the appearance
    member = models.ForeignKey(Member, related_name="appearances")

    # The match in which the member played
    match = models.ForeignKey(Match, related_name="appearances")

    # The number of goals the player scored
    goals = models.PositiveSmallIntegerField("Goals scored", default=0)

    # The number of own-goals the player scored
    own_goals = models.PositiveSmallIntegerField("Own-goals scored", default=0)

    # The following are nullable as we won't have this information for archive data
    green_card = models.NullBooleanField(default=None, help_text="Did the player receive a green card in the match?")
    yellow_card = models.NullBooleanField(default=None, help_text="Did the player receive a yellow card in the match?")
    red_card = models.NullBooleanField(default=None, help_text="Did the player receive a red card in the match?")

    objects = PassThroughManager.for_queryset_class(AppearanceQuerySet)()

    class Meta:
        app_label = 'matches'
        unique_together = ('member', 'match')       # A player can only make one appearance in a match!
        ordering = ['match', 'member']

    def __unicode__(self):
        return unicode("{} - {}".format(self.member, self.match))

    @classmethod
    def latest_match(cls, member):
        """ Returns the latest match the specified member played in, or
            None if they haven't played before.
        """
        try:
            last_app = Appearance.objects.by_member(member).select_related(
                'match__our_team', 'match__opp_team', 'match__venue', 'match__season', 'match__division__league', 'match__cup'
                ).latest('match__date')
        except Appearance.DoesNotExist:
            return None

        return cls.get_stats(last_app.match)

    @classmethod
    def get_stats(cls, match):
        match_stats = MatchStats(match)
        # Get all appearances for this match
        apps = Appearance.objects.filter(match=match).select_related('member__user')
        for app in apps:
            match_stats.add_appearance(app)

        # Get all award winners for this match
        award_winners = MatchAwardWinner.objects.select_related('member__user', 'award').filter(match=match)

        for award_winner in award_winners:
            match_stats.add_award_winner(award_winner)

        return match_stats
