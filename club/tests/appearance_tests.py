from django.test import TestCase
from django.db import IntegrityError
from datetime import datetime, date
from club.models import *
from club.models.choices import *
from django.contrib.auth.models import User

class AppearanceTest(TestCase):

    def setUp(self):
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
        self.test_season = Season(start=date(2012, 9, 1), end=date(2013, 8, 31))
        self.test_season.save()
        self.test_div_season = DivisionSeason(division=self.test_div, season=self.test_season)
        self.test_div_season.save()
        self.test_cup = Cup(name="Test cup")
        self.test_cup.save()
        self.test_cup_season = CupSeason(cup=self.test_cup, season=self.test_season)
        self.test_cup_season.save()
        self.test_match = FriendlyMatch(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=HomeAway.HOME, date=date(2012, 10, 1), season=self.test_season)
        self.test_match.save()
        self.user1=User(username="gm", first_name="Graham", last_name="McCulloch", email="test@test.com")
        self.user2=User(username="nh", first_name="Nathan", last_name="Humphreys", email="test2@test.com")
        self.user1.save()
        self.user2.save()
        self.test_member1 = Member(user=self.user1, gender=MemberGender.MALE, pref_position=MemberPosition.FORWARD)
        self.test_member1.save()
        self.test_member2 = Member(user=self.user2, gender=MemberGender.MALE, pref_position=MemberPosition.MIDFIELDER)
        self.test_member2.save()

    def test_appearances_can_be_added_and_removed(self):
        """ Tests that appearances can be added to the database and then removed """
        app1 = Appearance(member=self.test_member1, match=self.test_match, goals=3, own_goals=0)
        app2 = Appearance(member=self.test_member2, match=self.test_match, goals=0, own_goals=3)
        app1.save()
        app2.save()
        self.assertEqual(2, Appearance.objects.all().count())
        app1.delete()
        app2.delete()
        self.assertEqual(0, Appearance.objects.all().count())

    def test_a_member_cannot_appear_in_a_match_more_than_once(self):
        """"Tests that duplicate entries in the Appearances table are not allowed """
        app1 = Appearance(member=self.test_member1, match=self.test_match)
        app2 = Appearance(member=app1.member, match=app1.match)
        app1.save()
        self.assertRaises(IntegrityError, app2.save)
