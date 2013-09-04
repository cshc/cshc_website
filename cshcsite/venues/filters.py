import django_filters
from .models import Venue


CHOICES_FOR_IS_HOME = [
    ('', '----'),
    ('1', 'Home'),
    ('0', 'Away'),
]

BOOL_CHOICES = ((True, 'Home'), (False, 'Away'))

class VenueFilter(django_filters.FilterSet):
    is_home = django_filters.ChoiceFilter(choices=CHOICES_FOR_IS_HOME, label='Pitches')

    class Meta:
        model = Venue
        fields = ['is_home']

