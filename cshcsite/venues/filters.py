""" Venue filters used by the third-party django_filters app.

    Ref: http://django-filter.readthedocs.org/en/latest/usage.html#the-filter
"""

import django_filters
from venues.models import Venue


CHOICES_FOR_IS_HOME = [
    ('', '----'),
    ('1', 'Home'),
    ('0', 'Away'),
]


class VenueFilter(django_filters.FilterSet):
    """ Custom options for filtering a list of venues on the front-end."""
    is_home = django_filters.ChoiceFilter(choices=CHOICES_FOR_IS_HOME, label='Pitches')

    class Meta:
        """ Meta-info for the VenueFilter."""
        model = Venue
        fields = ['is_home']
