from django.conf.urls import patterns, url

from . import views, feeds

urlpatterns = patterns('',

    # E.g. '/teams/'
    url(r'^/?$',
        views.ClubTeamListView.as_view(),
        name="clubteam_list"
    ),

    # E.g. '/teams/southerners/'
    url(r'^southerners/$',
        views.SouthernersSeasonView.as_view(),
        name="southerners_league"
    ),

    # E.g. '/teams/southerners/2011-2012/'
    url(r'^southerners/(?P<season_slug>[-\w]+)/$',
        views.SouthernersSeasonView.as_view(),
        name="southerners_league_season"
    ),

    # E.g. '/teams/southerners/2011-2012/ajax/'
    url(r'^southerners/(?P<season_slug>[-\w]+)/ajax/$',
        views.SouthernersSeasonUpdateView.as_view(),
        name="southerners_league_season_update"
    ),

    # E.g. '/teams/m1/'
    url(r'^(?P<slug>[-\w]+)/$',
        views.ClubTeamDetailView.as_view(),
        name="clubteam_detail"
    ),

    # E.g. '/teams/m1/2011-2012/'
    url(r'^(?P<slug>[-\w]+)/(?P<season_slug>[-\w]+)/$',
        views.ClubTeamDetailView.as_view(),
        name="clubteam_season_detail"
    ),

    # E.g. /teams/m1.ics'
    url(r'^(?P<slug>[-\w]+).ics$',
        feeds.ClubTeamMatchICalFeed(),
        name="clubteam_ical_feed"
    ),

    # E.g. /teams/m1.rss'
    url(r'^(?P<slug>[-\w]+).rss$',
        feeds.RssClubTeamMatchReportsFeed(),
        name="clubteam_match_rss_feed"
    ),

    # E.g. '/teams/participation/23/ajax/'
    url(r'^participation/(?P<participation_id>\d+)/ajax/$',
        views.ParticipationUpdateView.as_view(),
        name="participation_update"
    ),

    # AJAX urls
     # E.g. /teams/m1/stats/3/ajax/'
    url(r'^(?P<slug>[-\w]+)/stats/(?P<season_pk>\d+)/ajax/$', views.ClubTeamStatsView.as_view(), name='clubteam_stats_ajax'),
    url(r'^(?P<slug>[-\w]+)/stats/(?P<season_pk>\d+)/ajax/scrape/$', views.ScrapeLeagueTableView.as_view(), name='refresh_league_table'),

)