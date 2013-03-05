from django.test import TestCase
from django.db import IntegrityError
from datetime import datetime, date
from club.models import Division, Season, League, DivisionSeason
from club.models.choices import *

class DivisionSeasonTest(TestCase):

    def setUp(self):
        self.test_url = "http://www.example.com"
        self.test_league = League(name="Test League", url=self.test_url)
        self.test_league.save()
        self.test_div1 = Division(name="Test Division 1", league=self.test_league, tables_url=self.test_url, fixtures_url=self.test_url, gender=TeamGender.MENS)
        self.test_div1.save()
        self.test_div2 = Division(name="Test Division 2", league=self.test_league, tables_url=self.test_url, fixtures_url=self.test_url, gender=TeamGender.MENS)
        self.test_div2.save()
        self.test_season = Season(start=date(2012, 9, 1), end=date(2013, 8, 31))
        self.test_season.save()

    def test_division_seasons_can_be_added_and_removed(self):
        """ Tests that division seasons can be added to the database and then removed """
        countBefore = DivisionSeason.objects.all().count()
        div_season1 = DivisionSeason(division=self.test_div1, season=self.test_season)
        div_season2 = DivisionSeason(division=self.test_div2, season=self.test_season)
        div_season1.save()
        div_season2.save()
        self.assertEqual(countBefore + 2, DivisionSeason.objects.all().count())
        div_season1.delete()
        div_season2.delete()
        self.assertEqual(countBefore, DivisionSeason.objects.all().count())

    def test_duplicate_division_seasons_are_not_allowed(self):
        """ Tests that the combination of division and season must be unique """
        div_season1 = DivisionSeason(division=self.test_div1, season=self.test_season)
        div_season2 = DivisionSeason(division=div_season1.division, season=div_season1.season)
        div_season1.save()
        self.assertRaises(IntegrityError, div_season2.save)


