from django.test import TestCase
from django.db import IntegrityError
from club.models import Club, Team
from club.models.choices import *

class TeamTest(TestCase):

    def setUp(self):
        self.test_url = "http://www.example.com"
        self.test_club = Club(name="Cambridge South", website=self.test_url)
        self.test_club.save()
        self.test_team = Team(club=self.test_club, gender=TeamGender.MENS, ordinal=TeamOrdinal.T1)

    def test_teams_can_be_added_and_removed(self):
        """ Tests that teams can be added to the database and then removed """
        team1 = Team(club=self.test_club, gender=TeamGender.MENS, ordinal=TeamOrdinal.T1)
        team2 = Team(club=self.test_club, gender=TeamGender.MENS, ordinal=TeamOrdinal.T2)
        team1.save()
        team2.save()
        self.assertEqual(2, Team.objects.all().count())
        team1.delete()
        team2.delete()
        self.assertEqual(0, Team.objects.all().count())

    def test_gender_and_ordinal_combination_must_be_unique_within_a_club(self):
        # Create two teams with the same club, gender and ordinal
        team1 = Team(club=self.test_club, gender=TeamGender.MENS, ordinal=TeamOrdinal.T1)
        team2 = Team(club=self.test_club, gender=TeamGender.MENS, ordinal=TeamOrdinal.T1)
        team1.save()
        # Insert should fail as both teams are in the same club and have the same gender and ordinal values
        self.assertRaises(IntegrityError, team2.save)
        # Now reset the 2nd team's ordinal value to something different
        team2.ordinal = TeamOrdinal.T2

        # This time it should be inserted fine
        team2.save()
        self.assertEqual(2, Team.objects.all().count())
