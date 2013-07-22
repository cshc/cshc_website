import logging
from django.test import TestCase
from django.db import IntegrityError
from datetime import date
from core.models import TeamGender, TeamOrdinal
from teams.models import ClubTeam
from opposition.models import Team, Club
from members.models import Member
from venues.models import Venue
from competitions.models import Season
from matches.models import Match
from .models import MatchAward, EndOfSeasonAward, MatchAwardWinner, EndOfSeasonAwardWinner

log = logging.getLogger(__name__)


class MatchAwardTest(TestCase):
    """Tests for Match Awards"""

    def test_match_awards_can_be_added_and_removed(self):
        """ Tests that match awards can be added to the database and then removed """
        countBefore = MatchAward.objects.all().count()
        award1 = MatchAward(name="Man of the match - test")
        award2 = MatchAward(name="Lemon of the match - test")
        award1.save()
        award2.save()
        self.assertEqual(countBefore + 2, MatchAward.objects.all().count())
        award1.delete()
        award2.delete()
        self.assertEqual(countBefore, MatchAward.objects.all().count())

    def test_award_names_must_be_unique(self):
        """ Tests that you cannot specify two awards with the same name """
        award1 = MatchAward(name="Man of the match - test")
        award2 = MatchAward(name=award1.name)
        award1.save()
        self.assertRaises(IntegrityError, award2.save)


class EndofSeasonAwardTest(TestCase):
    """Tests for End of Season Awards"""

    def test_end_of_season_awards_can_be_added_and_removed(self):
        """ Tests that end of season awards can be added to the database and then removed """
        countBefore = EndOfSeasonAward.objects.all().count()
        award1 = EndOfSeasonAward(name="1st team: Member of the season - test")
        award2 = EndOfSeasonAward(name="1st team: Most improved - test")
        award1.save()
        award2.save()
        self.assertEqual(countBefore + 2, EndOfSeasonAward.objects.all().count())
        award1.delete()
        award2.delete()
        self.assertEqual(countBefore, EndOfSeasonAward.objects.all().count())

    def test_award_names_must_be_unique(self):
        """ Tests that you cannot specify two awards with the same name """
        award1 = EndOfSeasonAward(name="1st team: Member of the season - test")
        award2 = EndOfSeasonAward(name=award1.name)
        award1.save()
        self.assertRaises(IntegrityError, award2.save)


class AwardWinnerTest(TestCase):
    """Tests for Award Winners"""

    def setUp(self):
        self.test_member1, m1_created = Member.objects.get_or_create(first_name="Graham", last_name="McCulloch", gender=Member.GENDER.Male, pref_position=Member.POSITION.Fwd)
        self.test_member2, m2_created = Member.objects.get_or_create(first_name="Nathan", last_name="Humphreys", gender=Member.GENDER.Male, pref_position=Member.POSITION.Mid)
        self.test_season, s_created = Season.objects.get_or_create(start=date(2012, 9, 1), end=date(2013, 8, 31))


class MatchAwardWinnerTest(AwardWinnerTest):
    """Tests for Match Award Winners"""

    def setUp(self):
        super(MatchAwardWinnerTest, self).setUp()
        self.test_url = "http://www.example.com"
        self.test_venue, v_created = Venue.objects.get_or_create(name="Venue 1", short_name="Ven1")
        self.test_their_club, c_created = Club.objects.get_or_create(name="Test Club 2", website=self.test_url)
        self.test_our_team, t1_created = ClubTeam.objects.get_or_create(short_name="Test1", long_name="Test team 1", gender=TeamGender.mens, ordinal=TeamOrdinal.T1, position=20)
        self.test_their_team, t2_created = Team.objects.get_or_create(club=self.test_their_club, gender=TeamGender.mens, ordinal=TeamOrdinal.T1, name="Opp team 1", short_name="Opp1")
        self.test_match, m_created = Match.objects.get_or_create(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=Match.HOME_AWAY.home, fixture_type=Match.FIXTURE_TYPE.Friendly, date=date(2012, 10, 1))
        self.test_match_award1, ma1_created = MatchAward.objects.get_or_create(name="Man of the match - test")
        self.test_match_award2, ma2_created = MatchAward.objects.get_or_create(name="Lemon of the match - test")

    def test_match_award_winners_can_be_added_and_removed(self):
        """ Tests that match award winners can be added to the database and then removed """
        countBefore = MatchAwardWinner.objects.all().count()
        awardWinner1 = MatchAwardWinner(match=self.test_match, award=self.test_match_award1, member=self.test_member1, comment="A note")
        awardWinner2 = MatchAwardWinner(match=self.test_match, award=self.test_match_award2, awardee="Some guy", comment="Another note")
        awardWinner1.save()
        awardWinner2.save()
        self.assertEqual(countBefore + 2, MatchAwardWinner.objects.all().count())
        awardWinner1.delete()
        awardWinner2.delete()
        self.assertEqual(countBefore, MatchAwardWinner.objects.all().count())

    def test_awardee_or_member_must_be_specified(self):
        """Test that you must specify either the member or the awardee for an award winner"""
        unidentified_award_winner = MatchAwardWinner(match=self.test_match, award=self.test_match_award1, comment="A note")
        self.assertRaises(IntegrityError, unidentified_award_winner.save)


class EndOfSeasonAwardWinnerTest(AwardWinnerTest):
    """Tests for End of Season Award Winners"""

    def setUp(self):
        super(EndOfSeasonAwardWinnerTest, self).setUp()
        self.test_award1, ea1_created = EndOfSeasonAward.objects.get_or_create(name="1st team: Member of the season - test")
        self.test_award2, ea2_created = EndOfSeasonAward.objects.get_or_create(name="1st team: Most improved - test")

    def test_end_of_season_award_winners_can_be_added_and_removed(self):
        """ Tests that end of season award winners can be added to the database and then removed """
        countBefore = EndOfSeasonAwardWinner.objects.all().count()
        awardWinner1 = EndOfSeasonAwardWinner(season=self.test_season, award=self.test_award1, member=self.test_member1, comment="A note")
        awardWinner2 = EndOfSeasonAwardWinner(season=self.test_season, award=self.test_award2, awardee="Some guy", comment="Another note")
        awardWinner1.save()
        awardWinner2.save()
        self.assertEqual(countBefore + 2, EndOfSeasonAwardWinner.objects.all().count())
        awardWinner1.delete()
        awardWinner2.delete()
        self.assertEqual(countBefore, EndOfSeasonAwardWinner.objects.all().count())
