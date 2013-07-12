import logging
from django.test import TestCase
from django.core.urlresolvers import reverse
from ..models import Venue
from ..views import VenueListView, VenueDetailView

log = logging.getLogger(__name__)


class VenueViewTest(TestCase):
    """Tests for views of the Venue model"""

    def setUp(self):
        self.test_venue_name = "My Venue"
        self.test_venue_short_name = "MyVen"
        self.test_venue, created = Venue.objects.get_or_create(name=self.test_venue_name, short_name=self.test_venue_short_name)

    def test_VenueListView(self):
        """ Tests that the VenueListView view contains the test venue """
        url = reverse('venue_list')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        retrieved_venue = response.context['venue_list'].get(name=self.test_venue_name)
        self.assertEquals(self.test_venue_name, retrieved_venue.name)

    def test_VenueDetailView(self):
        """ Tests that the VenueDetailView view contains the test venue """
        url = reverse('venue_detail', args=[self.test_venue.slug])
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)
        retrieved_venue = response.context['venue']
        self.assertEquals(self.test_venue_name, retrieved_venue.name)
