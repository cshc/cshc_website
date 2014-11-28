""" A few simple Django Views related to Venues.
"""

from django.views.generic import DetailView, ListView
from matches.models import Match
from venues.models import Venue
from venues.filters import VenueFilter


class VenueListView(ListView):
    """ A view that lists all venues, home and away."""
    model = Venue

    def get_context_data(self, **kwargs):
        context = super(VenueListView, self).get_context_data(**kwargs)
        # Ref: http://django-filter.readthedocs.org/en/latest/usage.html#the-view
        filter_qs = Venue.objects.all()
        context['filter'] = VenueFilter(self.request.GET, queryset=filter_qs)
        return context


class HomeVenueListView(VenueListView):
    """ A simple view that just lists home venues.

        Actually used as the 'about/directions' page.
    """
    queryset = Venue.objects.home_venues()
    template_name = "venues/venue_list_home.html"


class VenueDetailView(DetailView):
    """ A view that provides details of a particular venue."""
    model = Venue

    def get_context_data(self, **kwargs):
        context = super(VenueDetailView, self).get_context_data(**kwargs)

        venue = context["venue"]

        match_schedule = Match.objects.fixtures().filter(venue=venue).select_related('our_team', 'opp_team__club')
        context['match_schedule'] = match_schedule

        return context
