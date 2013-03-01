from django.test import TestCase
from django.db import IntegrityError
from datetime import datetime, date
from club.models import *
from club.models.choices import *
from django.contrib.auth.models import User

class MatchAwardTest(TestCase):

    def test_match_awards_can_be_added_and_removed(self):
        """ Tests that match awards can be added to the database and then removed """
        award1 = MatchAward(name="Man of the match")
        award2 = MatchAward(name="Lemon of the match")
        award1.save()
        award2.save()
        self.assertEqual(2, MatchAward.objects.all().count())
        award1.delete()
        award2.delete()
        self.assertEqual(0, MatchAward.objects.all().count())

    def test_award_names_must_be_unique(self):
        """ Tests that you cannot specify two awards with the same name """
        award1 = MatchAward(name="Man of the match")
        award2 = MatchAward(name=award1.name)
        award1.save()
        self.assertRaises(IntegrityError, award2.save)

class EndofSeasonAwardTest(TestCase):

    def test_end_of_season_awards_can_be_added_and_removed(self):
        """ Tests that end of season awards can be added to the database and then removed """
        award1 = EndOfSeasonAward(name="1st team: Member of the season")
        award2 = EndOfSeasonAward(name="1st team: Most improved")
        award1.save()
        award2.save()
        self.assertEqual(2, EndOfSeasonAward.objects.all().count())
        award1.delete()
        award2.delete()
        self.assertEqual(0, EndOfSeasonAward.objects.all().count())

    def test_award_names_must_be_unique(self):
        """ Tests that you cannot specify two awards with the same name """
        award1 = EndOfSeasonAward(name="1st team: Member of the season")
        award2 = EndOfSeasonAward(name=award1.name)
        award1.save()
        self.assertRaises(IntegrityError, award2.save)


class AwardWinnerTest(TestCase):

    def setUp(self):
        self.user1=User(username="gm", first_name="Graham", last_name="McCulloch", email="test@test.com")
        self.user2=User(username="nh", first_name="Nathan", last_name="Humphreys", email="test2@test.com")
        self.user1.save()
        self.user2.save()
        self.test_member1 = Member(user=self.user1, gender=MemberGender.MALE, pref_position=MemberPosition.FORWARD)
        self.test_member1.save()
        self.test_member2 = Member(user=self.user2, gender=MemberGender.MALE, pref_position=MemberPosition.MIDFIELDER)
        self.test_member2.save()
        self.test_season = Season(start=date(2012, 9, 1), end=date(2013, 8, 31))
        self.test_season.save()
        

class MatchAwardWinnerTest(AwardWinnerTest):

    def setUp(self):
        super(MatchAwardWinnerTest, self).setUp() 
        self.test_url = "http://www.example.com"
        self.test_venue = Venue(name="Venue 1", short_name="Ven1")
        self.test_our_club = Club(name="Cambridge South", website="http://www.cambridgesouthhockeyclub.co.uk")
        self.test_our_club.save()
        self.test_their_club = Club(name="Cambridge City", website="http://www.cambridgecityhc.org/")
        self.test_their_club.save()
        self.test_our_team = Team(club=self.test_our_club, gender=TeamGender.MENS, ordinal=TeamOrdinal.T1)
        self.test_our_team.save()
        self.test_their_team = Team(club=self.test_their_club, gender=TeamGender.MENS, ordinal=TeamOrdinal.T1)
        self.test_their_team.save()
        self.test_league = League(name="Test League", url=self.test_url)
        self.test_league.save()
        self.test_div = Division(name="Test Division", league=self.test_league, tables_url=self.test_url, fixtures_url=self.test_url, gender=TeamGender.MENS)
        self.test_div.save()
        self.test_div_season = DivisionSeason(division=self.test_div, season=self.test_season)
        self.test_div_season.save()
        self.test_cup = Cup(name="Test cup")
        self.test_cup.save()
        self.test_cup_season = CupSeason(cup=self.test_cup, season=self.test_season)
        self.test_cup_season.save()
        self.test_match = FriendlyMatch(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=HomeAway.HOME, date=date(2012, 10, 1), season=self.test_season)
        self.test_match.save()
        self.test_match_award1 = MatchAward(name="Man of the match")
        self.test_match_award1.save()
        self.test_match_award2 = MatchAward(name="Lemon of the match")
        self.test_match_award2.save()

    def test_match_award_winners_can_be_added_and_removed(self):
        """ Tests that match award winners can be added to the database and then removed """
        awardWinner1 = MatchAwardWinner(match=self.test_match, award=self.test_match_award1, member=self.test_member1, comment="A note")
        awardWinner2 = MatchAwardWinner(match=self.test_match, award=self.test_match_award2, awardee="Some guy", comment="Another note")
        awardWinner1.save()
        awardWinner2.save()
        self.assertEqual(2, MatchAwardWinner.objects.all().count())
        awardWinner1.delete()
        awardWinner2.delete()
        self.assertEqual(0, MatchAwardWinner.objects.all().count())   
        
    def test_awardee_or_member_must_be_specified(self):
        """Test that you must specify either the member or the awardee for an award winner"""
        unidentified_award_winner = MatchAwardWinner(match=self.test_match, award=self.test_match_award1, comment="A note")
        self.assertRaises(IntegrityError, unidentified_award_winner.save)

class EndOfSeasonAwardWinnerTest(AwardWinnerTest):

    def setUp(self):
        super(EndOfSeasonAwardWinnerTest, self).setUp() 
        self.test_award1 = EndOfSeasonAward(name="1st team: Member of the season")
        self.test_award1.save()
        self.test_award2 = EndOfSeasonAward(name="1st team: Most improved")
        self.test_award2.save()

    def test_end_of_season_award_winners_can_be_added_and_removed(self):
        """ Tests that end of season award winners can be added to the database and then removed """
        awardWinner1 = EndOfSeasonAwardWinner(season=self.test_season, award=self.test_award1, member=self.test_member1, comment="A note")
        awardWinner2 = EndOfSeasonAwardWinner(season=self.test_season, award=self.test_award2, awardee="Some guy", comment="Another note")
        awardWinner1.save()
        awardWinner2.save()
        self.assertEqual(2, EndOfSeasonAwardWinner.objects.all().count())
        awardWinner1.delete()
        awardWinner2.delete()
        self.assertEqual(0, EndOfSeasonAwardWinner.objects.all().count()) 
