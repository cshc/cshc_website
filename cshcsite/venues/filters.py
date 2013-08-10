import django_filters
from .models import Venue

class VenueFilter(django_filters.FilterSet):

    class Meta:
        model = Venue
        fields = ['is_home']

    def __init__(self, *args, **kwargs):
        super(VenueFilter, self).__init__(*args, **kwargs)
