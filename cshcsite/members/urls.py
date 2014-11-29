""" URL routing for the Member views.
"""

from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',

    # E.g. '/members/'                  - Lists all club members. Filterable.
    url(r'^$',
        views.MemberListView.as_view(),
        name="member_list"
    ),

    # E.g. '/members/32/'               - Details of a particular member
    url(r'^(?P<pk>\d+)/$',
        views.MemberDetailView.as_view(),
        name="member_detail"
    ),

    # Ajax requests
    # E.g. '/members/23/ajax/stats/'    - Member stats are retrived asynchronously for efficiency
    url(r'^(?P<pk>\d+)/ajax/stats/$',
        views.MemberStatsView.as_view(),
        name='member_stats_ajax'),
)
