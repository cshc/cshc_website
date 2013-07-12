import logging
from django.test import TestCase
from django.core.urlresolvers import reverse
from datetime import date
from core.models import TeamGender, TeamOrdinal
from teams.models import ClubTeam
from opposition.models import Team, Club
from competitions.models import Season
from venues.models import Venue
from ..models import Match

log = logging.getLogger(__name__)


class MatchViewTest(TestCase):
    """Tests for Match views"""

    def setUp(self):
        self.test_url = "http://www.example.com"
        self.test_venue, v_created = Venue.objects.get_or_create(name="Venue 1", short_name="Ven1")
        self.test_their_club, c_created = Club.objects.get_or_create(name="Test Club 2", website=self.test_url)
        self.test_our_team, t1_created = ClubTeam.objects.get_or_create(gender=TeamGender.mens, ordinal=TeamOrdinal.T1)
        self.test_their_team, t2_created = Team.objects.get_or_create(club=self.test_their_club, gender=TeamGender.mens, ordinal=TeamOrdinal.T1)
        self.test_season, s_created = Season.objects.get_or_create(start=date(2012, 9, 1), end=date(2013, 8, 31))
        self.test_match, m_created = Match.objects.get_or_create(our_team=self.test_our_team, opp_team=self.test_their_team, home_away=Match.HOME_AWAY.home, fixture_type=Match.FIXTURE_TYPE.Friendly, date=date(2012, 10, 1))

    def test_MatchListView(self):
        """ Tests that the MatchListView view contains the test match """
        url = reverse('match_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        retrieved_match = response.context['match_list'].get(pk=self.test_match.pk)
        self.assertEquals(self.test_match.pk, retrieved_match.pk)
        self.assertEquals(self.test_match.date, retrieved_match.date)

    def test_MatchDetailView(self):
        """ Tests that the MatchDetailView view contains the test match """
        url = reverse('match_detail', args=[self.test_match.pk])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        retrieved_match = response.context['match']
        self.assertEquals(self.test_match.pk, retrieved_match.pk)
        self.assertEquals(self.test_match.date, retrieved_match.date)


