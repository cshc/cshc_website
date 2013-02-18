from django.test import TestCase
from django.db import IntegrityError
from club.models import Club, Player, ClubAffiliation
from club.models.choices import PlayerGender, PlayerPosition
from datetime import datetime, date

class ClubAffiliationTest(TestCase):

    def setUp(self):
        self.test_player1 = Player(first_name="Graham", surname="McCulloch", gender=PlayerGender.MALE, pref_position=PlayerPosition.FORWARD)
        self.test_player1.save()
        self.test_player2 = Player(first_name="Mark", surname="Williams", gender=PlayerGender.MALE, pref_position=PlayerPosition.FORWARD)
        self.test_player2.save()
        self.test_url = "http://www.cambridgesouthhockeyclub.co.uk"
        self.test_club = Club(name="Cambridge South", website=self.test_url)
        self.test_club.save()

    def test_club_affiliations_can_be_added_and_removed(self):
        """ Tests that club affiliations can be added to the database and then removed """
        ca1 = ClubAffiliation(player=self.test_player1, club=self.test_club, start=date.today())
        ca2 = ClubAffiliation(player=self.test_player2, club=self.test_club, start=date.today())
        ca1.save()
        ca2.save()
        self.assertEqual(2, ClubAffiliation.objects.all().count())
        ca1.delete()
        ca2.delete()
        self.assertEqual(0, ClubAffiliation.objects.all().count())

    def test_club_affiliation_end_is_optional(self):
        """ Tests that you dont' have to specify the end (date left) for a club affiliation"""
        ca1 = ClubAffiliation(player=self.test_player1, club=self.test_club, start=date.today())
        self.assertEqual(None, ca1.end)
        ca1.save()
        self.assertEqual(1, ClubAffiliation.objects.all().count())

    def test_a_particular_player_can_be_affiliated_to_a_particular_club_multiple_times(self):
        """ Tests that the club and player combination is not unique (this is a many-to-many relationship """
        ca1 = ClubAffiliation(player=self.test_player1, club=self.test_club, start=date(2013, 1, 1))
        ca2 = ClubAffiliation(player=self.test_player1, club=self.test_club, start=date(2013, 1, 2))
        ca1.save()
        ca2.save()
        self.assertEqual(2, ClubAffiliation.objects.all().count())

    def test_a_club_affiliation_must_end_after_it_starts(self):
        """ Tests that the date the player left cannot be set to a date prior to the date the player joined """
        ca1 = ClubAffiliation(player=self.test_player1, club=self.test_club, start=date(2013, 1, 2))
        ca1.end = date(2013, 01, 01)
        self.assertRaises(IntegrityError, ca1.save)