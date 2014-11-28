""" These models keep track of all the times members won an award,
    be it a match award (MOM, LOM) or an end of season award.
"""

from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManager
from matches.models import Match
from members.models import Member
from competitions.models import Season
from awards.models.award import MatchAward, EndOfSeasonAward


class AwardWinnerQuerySet(QuerySet):
    """ Queries that relate to any Award Winners"""

    def by_member(self, member):
        """ Returns only items for the specified member"""
        return self.filter(member=member)


class MatchAwardWinnerQuerySet(AwardWinnerQuerySet):
    """ Queries that relate to Match Award Winners"""

    def mom(self):
        """Returns only Man of the Match award winners"""
        return self.filter(award__name=MatchAward.MOM)

    def lom(self):
        """Returns only Lemon of the Match award winners"""
        return self.filter(award__name=MatchAward.LOM)

    def by_match(self, match):
        """Returns only award winners for the specified match"""
        return self.filter(match=match)


class EndOfSeasonAwardWinnerQuerySet(AwardWinnerQuerySet):
    """ Queries that relate to End of Season Award Winners"""

    def by_season(self, season):
        """Returns only award winners for the specified season"""
        return self.filter(season=season)


class AwardWinner(models.Model):
    """Abstract base class for an award winner"""

    # The member that won this award. Either this field or the awardee field must
    # be filled in (but not both).
    member = models.ForeignKey(Member, related_name="%(app_label)s_%(class)s_awards",
                               null=True, blank=True, default=None,
                               help_text="(Leave blank if award winner is not a member)")

    # The name of the person that won this award (if not a member). Either this
    # field or the member field must be filled in (but not both).
    awardee = models.CharField("Award winner", max_length=255, blank=True,
                               help_text="Only use this field if the award winner is not a member")

    # A comment describing the award
    comment = models.TextField(help_text="Enter a short description of why this person " +
                               "received this award")

    class Meta:
        """ Meta-info on the AwardWinner model."""
        app_label = 'awards'
        abstract = True

    def clean(self):
        if self.member == None and (self.awardee == None or self.awardee == ""):
            raise ValidationError("You must specify either a member or an awardee " +
                                  "(if the awardee is not a member)")
        elif self.member != None and (self.awardee != None and self.awardee != ""):
            raise ValidationError("You cannot specify both a member and an awardee")

    def awardee_name(self):
        """ Returns either the awardee or the member's full name"""
        if self.member == None:
            return self.awardee
        return self.member.full_name()


class MatchAwardWinner(AwardWinner):
    """A winner of an award associated with matches"""

    # The match that the award winner won the award for
    match = models.ForeignKey(Match, related_name="award_winners")

    # The award that was won
    award = models.ForeignKey(MatchAward, related_name="winners")

    objects = PassThroughManager.for_queryset_class(MatchAwardWinnerQuerySet)()

    def __unicode__(self):
        return unicode("{} - {} ({})".format(self.award, self.awardee_name(), self.match.date))


class EndOfSeasonAwardWinner(AwardWinner):
    """A winner of an End of Season award"""

    # The season in which the award winner won the award
    season = models.ForeignKey(Season, related_name="award_winners")

    # The award that was won
    award = models.ForeignKey(EndOfSeasonAward, related_name="winners")

    objects = PassThroughManager.for_queryset_class(EndOfSeasonAwardWinnerQuerySet)()

    def __unicode__(self):
        return unicode("{} - {} ({})".format(self.award, self.awardee_name(), self.season))
