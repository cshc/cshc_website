import django_filters
from .models import Member


class MemberFilter(django_filters.FilterSet):

    class Meta:
        model = Member
        fields = ['first_name', 'last_name', 'gender', 'pref_position', 'is_current']

    def __init__(self, *args, **kwargs):
        super(MemberFilter, self).__init__(*args, **kwargs)
