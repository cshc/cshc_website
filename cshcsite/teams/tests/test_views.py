import logging
from datetime import date
from django.test import TestCase
from django.core.urlresolvers import reverse
from core.models import TeamGender, TeamOrdinal
from competitions.models import Season
from ..models import ClubTeam

log = logging.getLogger(__name__)


class ClubTeamViewTest(TestCase):
    """Tests for views that relate to the ClubTeam model"""

    def setUp(self):
        self.test_season, s_created = Season.objects.get_or_create(start=date(2012, 9, 1), end=date(2013, 8, 31))
        self.test_clubteam, c_created = ClubTeam.objects.get_or_create(short_name="Test", long_name="Test team", gender=TeamGender.mens, ordinal=TeamOrdinal.T1, position=20)

    def test_ClubTeamListView(self):
        """ Tests that the ClubTeamListView view contains the test ClubTeam """
        url = reverse('clubteam_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        retrieved_clubteam = response.context['teams'][0][1][0]
        self.assertClubTeamEquals(self.test_clubteam, retrieved_clubteam)

    def test_ClubTeamDetailView(self):
        """ Tests that the ClubTeamDetailView view contains the test ClubTeam """
        url = reverse('clubteam_detail', args=[self.test_clubteam.slug])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        retrieved_clubteam = response.context['clubteam']
        self.assertClubTeamEquals(self.test_clubteam, retrieved_clubteam)

    def assertClubTeamEquals(self, team1, team2):
        self.assertEquals(team1.pk, team2.pk)
        self.assertEquals(team1.gender, team2.gender)
        self.assertEquals(team1.ordinal, team2.ordinal)
