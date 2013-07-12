import logging
from django.test import TestCase
from django.db import IntegrityError
from core.models import  TeamGender
from ..models import League, Division

log = logging.getLogger(__name__)


class DivisionTest(TestCase):
    """Tests for the Division model"""

    def setUp(self):
        self.test_url = "http://www.example.com"
        self.test_league = League(name="Test League", url=self.test_url)
        self.test_league.save()
        self.test_div = Division(name="Test Division", league=self.test_league, gender=TeamGender.mens)

    def test_divisions_can_be_added_and_removed(self):
        """ Tests that divisions can be added to the database and then removed """
        countBefore = Division.objects.all().count()
        div1 = Division(name="Test Division 1", league=self.test_league, gender=TeamGender.mens)
        div2 = Division(name="Test Division 2", league=self.test_league, gender=TeamGender.mens)
        div1.save()
        div2.save()
        self.assertEqual(countBefore + 2, Division.objects.all().count())
        div1.delete()
        div2.delete()
        self.assertEqual(countBefore, Division.objects.all().count())

    def test_division_name_cannot_be_none(self):
        """ Tests that you must specify the name of the division """
        self.test_div.name = None
        self.assertEqual(None,self.test_div.name)
        self.assertRaisesMessage(IntegrityError, "competitions_division.name may not be NULL", self.test_div.save)

    def test_division_name_must_be_unique_within_league(self):
        """ Tests that you can't have two divisions in the same league with the same name """
        countBefore = Division.objects.all().count()
        self.test_div.save()
        # Create a new division with the same name and league
        test_div2 = Division(name=self.test_div.name, league=self.test_div.league, gender=TeamGender.mens)

        # Insert should fail as both divisions are in the same league and have the same name
        self.assertRaises(IntegrityError, test_div2.save)

        # Now create a 2nd league and link the new division to this league instead
        test_league2 = League(name="Test League 2", url=self.test_url)
        test_league2.save()
        test_div2.league = test_league2

        # This time it should be inserted fine
        test_div2.save()
        self.assertEqual(countBefore + 2, Division.objects.all().count())
        # (Ignore the trivial case where both have the same league but different names)
