""" Member filters used by the third-party django_filters app.

    Ref: http://django-filter.readthedocs.org/en/latest/usage.html#the-filter
"""

import django_filters
from members.models import Member


class MemberFilter(django_filters.FilterSet):
    """ Custom options for filtering a list of members on the front-end."""

    class Meta:
        """ Meta-info for the MemberFilter"""
        model = Member
        fields = ['first_name', 'last_name', 'gender', 'pref_position', 'is_current']
