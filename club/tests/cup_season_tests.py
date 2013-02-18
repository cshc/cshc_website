from django.test import TestCase
from django.db import IntegrityError
from datetime import datetime, date
from club.models import Cup, Season, League, CupSeason
from club.models.choices import *

class CupSeasonTest(TestCase):

    def setUp(self):
        self.test_cup1 = Cup(name="Cup 1")
        self.test_cup2 = Cup(name="Cup 2")
        self.test_cup1.save()
        self.test_cup2.save()
        self.test_season = Season(start=date(2012, 9, 1), end=date(2013, 8, 31))
        self.test_season.save()

    def test_cup_seasons_can_be_added_and_removed(self):
        """ Tests that cup seasons can be added to the database and then removed """
        cup_season1 = CupSeason(cup=self.test_cup1, season=self.test_season)
        cup_season2 = CupSeason(cup=self.test_cup2, season=self.test_season)
        cup_season1.save()
        cup_season2.save()
        self.assertEqual(2, CupSeason.objects.all().count())
        cup_season1.delete()
        cup_season2.delete()
        self.assertEqual(0, CupSeason.objects.all().count())

    def test_duplicate_cup_seasons_are_not_allowed(self):
        """ Tests that the combination of cup and season must be unique """
        cup_season1 = CupSeason(cup=self.test_cup1, season=self.test_season)
        cup_season2 = CupSeason(cup=cup_season1.cup, season=cup_season1.season)
        cup_season1.save()
        self.assertRaises(IntegrityError, cup_season2.save)


