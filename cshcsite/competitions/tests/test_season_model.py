import logging
from django.test import TestCase
from django.db import IntegrityError
from datetime import datetime, date, timedelta
from ..models import Season

log = logging.getLogger(__name__)


class SeasonTest(TestCase):
    """Tests for the Season model"""

    def test_seasons_can_be_added_and_removed(self):
        """ Tests that seasons can be added to the database and then removed """
        countBefore = Season.objects.all().count()
        season1 = Season(start=date(2011, 9, 1), end=date(2012, 8, 31))
        season2 = Season(start=date(2012, 9, 1), end=date(2013, 8, 31))
        season1.save()
        season2.save()
        self.assertEqual(countBefore + 2, Season.objects.all().count())
        season1.delete()
        season2.delete()
        self.assertEqual(countBefore, Season.objects.all().count())

    def test_a_season_must_end_after_it_starts(self):
        """ Tests that the start date of a season must be prior to the end date """
        season1 = Season(start=date(2011, 9, 1), end=date(2011, 9, 1))
        self.assertRaises(IntegrityError, season1.save)

    def test_seasons_cannot_overlap(self):
        """ Tests that the start date and end date of a season cannot fall within another season's timeframe"""
        season1 = Season(start=date(2011, 9, 1), end=date(2012, 8, 31))
        season1.save()
        season2 = Season(start=season1.end - timedelta(days=2), end=season1.end + timedelta(days=2))
        self.assertRaises(IntegrityError, season2.save)
        season2 = Season(start=season1.start - timedelta(days=2), end=season1.start + timedelta(days=2))
        self.assertRaises(IntegrityError, season2.save)