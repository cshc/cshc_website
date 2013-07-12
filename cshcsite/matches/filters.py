from django.forms import extras
import django_filters
from .models import Match


class MatchFilter(django_filters.FilterSet):

    class Meta:
        model = Match
        fields = ['date', 'our_team', 'opp_team', 'venue', 'season', 'players']

    def __init__(self, *args, **kwargs):
        super(MatchFilter, self).__init__(*args, **kwargs)
        #self.filters['season'].extra.update(
        #    {'empty_label': 'Any season'})
        self.filters['opp_team'].label = 'Opposition'
        self.filters['players'].label = 'Player'
        self.filters['date'].widget = extras.SelectDateWidget
