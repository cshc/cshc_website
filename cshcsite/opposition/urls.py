from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
    # E.g. 'opposition/clubs/'
    url(r'^clubs/$',
        views.ClubListView.as_view(),
        name="opposition_club_list"
    ),

    # E.g. 'opposition/clubs/ajax/'
    url(r'^clubs/ajax/$',
        views.ClubStatsUpdateView.as_view(),
        name="clubstats_update"
    ),

    # E.g. 'opposition/clubs/cambridge-city/'
    url(r'^clubs/(?P<slug>[-\w]+)/$',
        views.ClubDetailView.as_view(),
        name="opposition_club_detail"
    ),

    # Not implemented

    # E.g. 'opposition/teams/'
    # url(r'^teams/$',
    #     views.TeamListView.as_view(),
    #     name="opposition_team_list"
    # ),

    # E.g. 'opposition/teams/cambridge-city-mens-1sts/'
    # url(r'^teams/(?P<slug>[-\w]+)/$',
    #     views.TeamDetailView.as_view(),
    #     name="opposition_team_detail"
    # ),
)
