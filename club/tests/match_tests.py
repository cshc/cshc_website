from django.test import TestCase
from django.db import IntegrityError
from datetime import datetime, date
from club.models import *
from club.models.choices import *

class MatchTest(TestCase):

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


class FriendlyMatchTest(MatchTest):

    def test_friendly_matches_can_be_added_and_removed(self):
        """ Tests that friendly matches can be added to the database and then removed """
        match1 = FriendlyMatch(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=HomeAway.HOME, date=date(2012, 10, 1), season=self.test_season)
        match2 = FriendlyMatch(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=HomeAway.AWAY, date=date(2012, 10, 8), season=self.test_season)
        match1.save()
        match2.save()
        self.assertEqual(2, Match.objects.all().count())
        self.assertEqual(2, FriendlyMatch.objects.all().count())
        match1.delete()
        match2.delete()
        self.assertEqual(0, Match.objects.all().count())
        self.assertEqual(0, FriendlyMatch.objects.all().count())


class CupMatchTest(MatchTest):

    def test_cup_matches_can_be_added_and_removed(self):
        """ Tests that cup_matches can be added to the database and then removed """
        match1 = CupMatch(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=HomeAway.HOME, date=date(2012, 10, 1), cup_season=self.test_cup_season)
        match2 = CupMatch(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=HomeAway.AWAY, date=date(2012, 10, 8), cup_season=self.test_cup_season)
        match1.save()
        match2.save()
        self.assertEqual(2, Match.objects.all().count())
        self.assertEqual(2, CupMatch.objects.all().count())
        match1.delete()
        match2.delete()
        self.assertEqual(0, Match.objects.all().count())
        self.assertEqual(0, CupMatch.objects.all().count())


class DivisionMatchTest(MatchTest):

    def test_division_matches_can_be_added_and_removed(self):
        """ Tests that division matches can be added to the database and then removed """
        match1 = DivisionMatch(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=HomeAway.HOME, date=date(2012, 10, 1), div_season=self.test_div_season)
        match2 = DivisionMatch(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=HomeAway.AWAY, date=date(2012, 10, 8), div_season=self.test_div_season)
        match1.save()
        match2.save()
        self.assertEqual(2, Match.objects.all().count())
        self.assertEqual(2, DivisionMatch.objects.all().count())
        match1.delete()
        match2.delete()
        self.assertEqual(0, Match.objects.all().count())
        self.assertEqual(0, DivisionMatch.objects.all().count())