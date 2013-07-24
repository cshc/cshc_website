import logging
from django.test import TestCase
from django.core.urlresolvers import reverse
from core.models import TeamGender
from ..models import Club, Team
from ..stats import update_all_club_stats

log = logging.getLogger(__name__)


class ClubViewTest(TestCase):
    """Tests for the Club views"""

    def setUp(self):
        self.test_club_name = "Test Club"
        self.test_club, created = Club.objects.get_or_create(name=self.test_club_name)
        update_all_club_stats()

    def test_ClubListView(self):
        """ Tests that the ClubListView view contains the test club """
        url = reverse('opposition_club_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        retrieved_club = filter(lambda x: x.club.pk == self.test_club.pk, response.context['clubstats_list'])[0]
        self.assertEquals(self.test_club_name, retrieved_club.club.name)

    def test_ClubDetailView(self):
        """ Tests that the ClubDetailView view contains the test venue """
        url = reverse('opposition_club_detail', args=[self.test_club.slug])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        retrieved_club = response.context['club']
        self.assertEquals(self.test_club_name, retrieved_club.name)


class TeamViewTest(TestCase):
    """Tests for the Team views"""

    def setUp(self):
        self.test_club_name = "Test Club"
        self.test_club, club_created = Club.objects.get_or_create(name=self.test_club_name)
        self.test_team, team_created = Team.objects.get_or_create(club=self.test_club, gender=TeamGender.Mens, name="Test team 1", short_name="T1")

    def test_TeamListView(self):
        """ Tests that the TeamListView view contains the test team """
        url = reverse('opposition_team_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        retrieved_team = response.context['team_list'].get(pk=self.test_team.pk)
        self.assertEquals(self.test_club_name, retrieved_team.club.name)
        self.assertEquals(self.test_team.gender, retrieved_team.gender)

    def test_TeamDetailView(self):
        """ Tests that the TeamDetailView view contains the test team """
        url = reverse('opposition_team_detail', args=[self.test_team.slug])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        retrieved_team = response.context['team']
        self.assertEquals(self.test_club_name, retrieved_team.club.name)
        self.assertEquals(self.test_team.gender, retrieved_team.gender)
