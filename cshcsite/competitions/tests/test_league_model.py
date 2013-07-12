import logging
from django.test import TestCase
from django.db import IntegrityError
from ..models import League

log = logging.getLogger(__name__)


class LeagueTest(TestCase):
    """Tests for the League model"""

    def setUp(self):
        self.test_url = "http://www.example.com"

    def test_new_leagues_can_be_added_and_removed(self):
        """ Tests new leagues can be added to the database and then removed """
        countBefore = League.objects.all().count()
        league1 = League(name="Test League", url=self.test_url)
        league2 = League(name="Test League 2", url=self.test_url)
        league1.save()
        league2.save()
        self.assertEqual(countBefore + 2, League.objects.all().count())
        league1.delete()
        league2.delete()
        self.assertEqual(countBefore, League.objects.all().count())

    def test_league_name_must_be_specified(self):
        """ Tests that you must specify the name of the league """
        league_with_no_name = League(url=self.test_url)
        self.assertEqual(None, league_with_no_name.name)
        self.assertRaises(IntegrityError, league_with_no_name.save)

    def test_league_url_is_optional(self):
        """ Tests that you don't have to specify the url of the league """
        countBefore = League.objects.all().count()
        league_with_no_url = League(name="Test League")
        league_with_no_url.save()
        self.assertEqual("", league_with_no_url.url)
        self.assertEqual(countBefore + 1, League.objects.all().count())

    def test_league_names_must_be_unique(self):
        """ Tests that you can't have two leagues with the same name """
        league1 = League(name="Test League", url=self.test_url)
        league2 = League(name="Test League", url=self.test_url)
        league1.save()
        self.assertRaises(IntegrityError, league2.save)