import logging
from django.test import TestCase
from django.db import IntegrityError
from ..models import Club, Team
from core.models import TeamGender, TeamOrdinal

log = logging.getLogger(__name__)


class TeamTest(TestCase):
    """Tests for the Team model"""

    def setUp(self):
        self.test_url = "http://www.example.com"
        self.test_club, club_created = Club.objects.get_or_create(name="Test Club 1", website=self.test_url)
        self.test_team = Team(club=self.test_club, gender=TeamGender.mens, ordinal=TeamOrdinal.T1)

    def test_teams_can_be_added_and_removed(self):
        """ Tests that teams can be added to the database and then removed """
        countBefore = Team.objects.all().count()
        team1 = Team(club=self.test_club, gender=TeamGender.mens, ordinal=TeamOrdinal.T1)
        team2 = Team(club=self.test_club, gender=TeamGender.mens, ordinal=TeamOrdinal.T2)
        team1.save()
        team2.save()
        self.assertEqual(countBefore + 2, Team.objects.all().count())
        team1.delete()
        team2.delete()
        self.assertEqual(countBefore, Team.objects.all().count())

    def test_gender_and_ordinal_combination_must_be_unique_within_a_club(self):
        """Tests that you can't create two teams in the same club with the same gender and ordinal"""
        countBefore = Team.objects.all().count()
        team1 = Team(club=self.test_club, gender=TeamGender.mens, ordinal=TeamOrdinal.T1)
        team2 = Team(club=self.test_club, gender=TeamGender.mens, ordinal=TeamOrdinal.T1)
        team1.save()
        # Insert should fail as both teams are in the same club and have the same gender and ordinal values
        self.assertRaises(IntegrityError, team2.save)
        # Now reset the 2nd team's ordinal value to something different
        team2.ordinal = TeamOrdinal.T2

        # This time it should be inserted fine
        team2.save()
        self.assertEqual(countBefore + 2, Team.objects.all().count())
