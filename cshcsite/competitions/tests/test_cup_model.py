import logging
from django.test import TestCase
from django.db import IntegrityError
from ..models import Cup, League

log = logging.getLogger(__name__)


class CupTest(TestCase):
    """Tests for the Cup model"""

    def setUp(self):
        self.test_url = "http://www.example.com"
        self.test_league = League(name="Test League", url=self.test_url)
        self.test_league.save()
        
    def test_cups_can_be_added_and_removed(self):
        """ Tests that cups can be added to and removed from the database """
        countBefore = Cup.objects.all().count()
        cup1 = Cup(name="Test cup 1", league=self.test_league)
        cup2 = Cup(name="Test cup 2", league=self.test_league)
        cup1.save()
        cup2.save()
        self.assertEqual(countBefore + 2, Cup.objects.all().count())
        cup1.delete()
        cup2.delete()
        self.assertEqual(countBefore, Cup.objects.all().count())

    def test_cup_name_must_be_specified(self):
        """ Tests that you must specify the name of the cup """
        cup_with_no_name = Cup(league=self.test_league)
        self.assertEqual(None, cup_with_no_name.name)
        self.assertRaises(IntegrityError, cup_with_no_name.save)

    def test_cup_league_is_optional(self):
        """ Tests that you don't have to specify the league of the cup """
        countBefore = Cup.objects.all().count()
        cup_with_no_league = Cup(name="Test cup")
        cup_with_no_league.save()
        self.assertEqual(None, cup_with_no_league.league)
        self.assertEqual(countBefore + 1, Cup.objects.all().count())

    def test_cup_names_must_be_unique(self):
        """ Tests that you can't have two cups with the same name """
        cup1 = Cup(name="Test cup", league=self.test_league)
        cup2 = Cup(name=cup1.name, league=self.test_league)
        cup1.save()
        self.assertRaises(IntegrityError, cup2.save)
