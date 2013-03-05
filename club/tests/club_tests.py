from django.test import TestCase
from django.db import IntegrityError
from club.models import Club
from club.models.choices import *

class ClubTest(TestCase):

    def setUp(self):
        self.test_url = "http://www.example.com"
        self.test_club = Club(name="Test Club 1", website=self.test_url)
        
    def test_clubs_can_be_added_and_removed(self):
        """ Tests that clubs can be added to the database and then removed """
        countBefore = Club.objects.all().count()
        club1 = Club(name="Test Club 1", website=self.test_url)
        club2 = Club(name="Test Club 2", website=self.test_url)
        club1.save()
        club2.save()
        self.assertEqual(countBefore + 2, Club.objects.all().count())
        club1.delete()
        club2.delete()
        self.assertEqual(countBefore, Club.objects.all().count())

    def test_club_name_cannot_be_none(self):
        """ Tests that you must specify the name of the club """
        self.test_club.name = None
        self.assertEqual(None,self.test_club.name)
        self.assertRaisesMessage(IntegrityError, "club_club.name may not be NULL", self.test_club.save)

    def test_club_website_is_optional(self):
        """ Tests that you dont' have to specify the website url for a club """
        countBefore = Club.objects.all().count()
        self.test_club.website = None
        self.test_club.save()
        self.assertEqual(countBefore + 1, Club.objects.all().count())

    def test_club_names_must_be_unique(self):
        """ Tests that you can't have two clubs with the same name """
        club1 = Club(name="Test Club", website=self.test_url)
        club2 = Club(name="Test Club", website=self.test_url)
        club1.save()
        self.assertRaises(IntegrityError, club2.save)
