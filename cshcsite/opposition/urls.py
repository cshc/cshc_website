""" URL routing related to the opposition.
"""

from django.conf.urls import patterns, url
from opposition import views


urlpatterns = patterns('',

    # E.g. 'opposition/clubs/'                  - List of all oppostion clubs (including statistics)
    url(r'^clubs/$',
        views.ClubListView.as_view(),
        name="opposition_club_list"
    ),

    # E.g. 'opposition/clubs/ajax/'             - AJAX endpoint for refreshing the club stats
    url(r'^clubs/ajax/$',
        views.ClubStatsUpdateView.as_view(),
        name="clubstats_update"
    ),

    # E.g. 'opposition/clubs/cambridge-city/'   - Details of a particular opposition club
    url(r'^clubs/(?P<slug>[-\w]+)/$',
        views.ClubDetailView.as_view(),
        name="opposition_club_detail"
    ),
)
