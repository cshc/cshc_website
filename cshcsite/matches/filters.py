from django.forms import extras
import django_filters
from .models import Match
from competitions.models import Season

CHOICES_FOR_HOME_AWAY = [
    ('', '---------'),
]
CHOICES_FOR_HOME_AWAY.extend(list(Match.HOME_AWAY))

CHOICES_FOR_FIXTURE_TYPE = [
    ('', '---------'),
]
CHOICES_FOR_FIXTURE_TYPE.extend(list(Match.FIXTURE_TYPE))

class MatchFilter(django_filters.FilterSet):

    class Meta:
        model = Match
        fields = ['date', 'our_team', 'opp_team', 'venue', 'season', 'players', 'home_away', 'fixture_type', 'division']

    def __init__(self, *args, **kwargs):
        super(MatchFilter, self).__init__(*args, **kwargs)
        #self.filters['season'].extra.update(
        #    {'empty_label': 'Any season'})
        self.filters['opp_team'].label = 'Opposition'
        self.filters['players'].label = 'Player'
        seasons = list(Season.objects.order_by('start'))
        earliest_season = seasons[0]
        latest_season = seasons[-1]
        self.filters['date'].widget = extras.SelectDateWidget(years=range(earliest_season.start.year, latest_season.end.year))
        self.filters['home_away'].extra.update({ 'choices': CHOICES_FOR_HOME_AWAY })
        self.filters['fixture_type'].extra.update({ 'choices': CHOICES_FOR_FIXTURE_TYPE })