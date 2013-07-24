import logging
from django.test import TestCase
from ..models import Club, Team
from core.models import TeamGender

log = logging.getLogger(__name__)


class TeamTest(TestCase):
    """Tests for the Team model"""

    def setUp(self):
        self.test_url = "http://www.example.com"
        self.test_club, club_created = Club.objects.get_or_create(name="Test Club 1", website=self.test_url)
        self.test_team = Team(club=self.test_club, gender=TeamGender.Mens, name="Test Team 1", short_name="T1")

    def test_teams_can_be_added_and_removed(self):
        """ Tests that teams can be added to the database and then removed """
        countBefore = Team.objects.all().count()
        team1 = Team(club=self.test_club, gender=TeamGender.Mens, name="Test Team 1", short_name="T1")
        team2 = Team(club=self.test_club, gender=TeamGender.Mens, name="Test Team 2", short_name="T2")
        team1.save()
        team2.save()
        self.assertEqual(countBefore + 2, Team.objects.all().count())
        team1.delete()
        team2.delete()
        self.assertEqual(countBefore, Team.objects.all().count())
