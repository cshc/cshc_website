from django.test import TestCase
from django.db import IntegrityError
from club.models import League, Division
from club.models.choices import *

class DivisionTest(TestCase):

    def setUp(self):
        self.test_url = "http://www.example.com"
        self.test_league = League(name="Test League", url=self.test_url)
        self.test_league.save()
        self.test_div = Division(name="Test Division", league=self.test_league, tables_url=self.test_url, fixtures_url=self.test_url, gender=TeamGender.MENS)
        self.assertEqual(0, Division.objects.all().count())

    def test_divisions_can_be_added_and_removed(self):
        """ Tests that divisions can be added to the database and then removed """
        div1 = Division(name="Test Division 1", league=self.test_league, tables_url=self.test_url, fixtures_url=self.test_url, gender=TeamGender.MENS)
        div2 = Division(name="Test Division 2", league=self.test_league, tables_url=self.test_url, fixtures_url=self.test_url, gender=TeamGender.MENS)
        div1.save()
        div2.save()
        self.assertEqual(2, Division.objects.all().count())
        div1.delete()
        div2.delete()
        self.assertEqual(0, Division.objects.all().count())

    def test_division_name_cannot_be_none(self):
        """ Tests that you must specify the name of the division """
        self.test_div.name = None
        self.assertEqual(None,self.test_div.name)
        self.assertRaisesMessage(IntegrityError, "club_division.name may not be NULL", self.test_div.save)

    def test_division_tables_and_fixtures_urls_are_optional(self):
        """ Tests that you dont' have to specify the tables and fixtures urls for a division """
        self.test_div.tables_url = None
        self.test_div.fixtures_url = None
        self.test_div.save()
        self.assertEqual(1, Division.objects.all().count())

    def test_prom_rel_divs_are_optional(self):
        """ Tests that you don't have to specify promotion or relegation division foreign keys """
        self.assertEqual(None, self.test_div.promotion_div)
        self.assertEqual(None, self.test_div.relegation_div)
        self.test_div.save()
        self.assertEqual(1, Division.objects.all().count())

    def test_division_name_must_be_unique_within_league(self):
        """ Tests that you can't have two divisions in the same league with the same name """
        self.test_div.save()
        # Create a new division with the same name and league
        test_div2 = Division(name=self.test_div.name, league=self.test_div.league, tables_url=self.test_url, fixtures_url=self.test_url, gender=TeamGender.MENS)

        # Insert should fail as both divisions are in the same league and have the same name
        self.assertRaises(IntegrityError, test_div2.save)

        # Now create a 2nd league and link the new division to this league instead
        test_league2 = League(name="Test League 2", url=self.test_url)
        test_league2.save()
        test_div2.league = test_league2

        # This time it should be inserted fine
        test_div2.save()
        self.assertEqual(2, Division.objects.all().count())
        # (Ignore the trivial case where both have the same league but different names)

    def test_prom_rel_divs_cannot_be_the_same(self):
        """ Tests that you can't set the promotion and relegation division to be the same """
        test_div2 = Division(name="Another div", league=self.test_div.league, tables_url=self.test_url, fixtures_url=self.test_url, gender=TeamGender.MENS)
        test_div2.save()
        # Point both promotion and relegation foreign keys at the same division
        self.test_div.promotion_div = test_div2
        self.test_div.relegation_div = test_div2
        self.assertRaises(IntegrityError, self.test_div.save)