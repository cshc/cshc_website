from django.views.generic import DetailView, ListView
from matches.models import Match
from .models import Venue

class VenueListView(ListView):
    model = Venue


class HomeVenueListView(VenueListView):
    queryset = Venue.objects.home_venues()
    template_name = "venues/venue_list_home.html"


class VenueDetailView(DetailView):
    model = Venue

    def get_context_data(self, **kwargs):
        context = super(VenueDetailView, self).get_context_data(**kwargs)
    
        venue = context["venue"]

        match_schedule = Match.objects.fixtures().filter(venue=venue).select_related('our_team', 'opp_team__club')
        context['match_schedule'] = match_schedule
        
        return context