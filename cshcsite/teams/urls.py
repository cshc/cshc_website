""" URL routing for views relating to teams.
"""

from django.conf.urls import patterns, url
from teams import views, feeds


urlpatterns = patterns('',

    # E.g. '/teams/'                            - List of all CSHC teams
    url(r'^/?$',
        views.ClubTeamListView.as_view(),
        name="clubteam_list"
    ),

    # E.g. '/teams/playing-record/'             - The playing records through the seasons of each team
    url(r'^playing-record/$',
        views.PlayingRecordView.as_view(),
        name="playing_record"
    ),

    # E.g. '/teams/playing-record/ajax/'        - AJAX-only: Updates and refreshes the playing records of each team
    url(r'^playing-record/ajax/$',
        views.PlayingRecordUpdateView.as_view(),
        name="playing_record_update"
    ),

    # E.g. '/teams/southerners/'                - Statistics table comparing the performance of CSHC teams this season
    url(r'^southerners/$',
        views.SouthernersSeasonView.as_view(),
        name="southerners_league"
    ),

    # E.g. '/teams/southerners/2011-2012/'      - Statistics table comparing the performance of CSHC teams in a previous season
    url(r'^southerners/(?P<season_slug>[-\w]+)/$',
        views.SouthernersSeasonView.as_view(),
        name="southerners_league_season"
    ),

    # E.g. '/teams/southerners/2011-2012/ajax/' - AJAX-only: Updates and refreshes the Southerners statistics
    url(r'^southerners/(?P<season_slug>[-\w]+)/ajax/$',
        views.SouthernersSeasonUpdateView.as_view(),
        name="southerners_league_season_update"
    ),

    # E.g. '/teams/m1/'                         - Details of a particular CSHC team (including the team's playing record) for the current season
    url(r'^(?P<slug>[-\w]+)/$',
        views.ClubTeamDetailView.as_view(),
        name="clubteam_detail"
    ),

    # E.g. '/teams/m1/2011-2012/'               - Details of a particular CSHC team (including the team's playing record) for a previous season
    url(r'^(?P<slug>[-\w]+)/(?P<season_slug>[-\w]+)/$',
        views.ClubTeamDetailView.as_view(),
        name="clubteam_season_detail"
    ),

    # E.g. /teams/m1.ics'                       - Calendar feed of a particular team's matches
    url(r'^(?P<slug>[-\w]+).ics$',
        feeds.ClubTeamMatchICalFeed(),
        name="clubteam_ical_feed"
    ),

    # E.g. /teams/m1.rss'                       - RSS feed of a particular team's match reports
    url(r'^(?P<slug>[-\w]+).rss$',
        feeds.RssClubTeamMatchReportsFeed(),
        name="clubteam_match_rss_feed"
    ),

    # E.g. '/teams/participation/23/ajax/'      - AJAX-only: Updates and refreshes the playing record stats for a particular team in a particular season
    url(r'^participation/(?P<participation_id>\d+)/ajax/$',
        views.ParticipationUpdateView.as_view(),
        name="participation_update"
    ),

    # E.g. '/teams/m1/stats/3/ajax/'             - AJAX-only: Retrieves fixture list, league table and squad membership for a particular team/season
    url(r'^(?P<slug>[-\w]+)/stats/(?P<season_pk>\d+)/ajax/$',
        views.ClubTeamStatsView.as_view(),
        name='clubteam_stats_ajax'),

    # E.g. '/teams/m1/stats/3/ajax/scrape/'      - AJAX-only: Scrapes the external league table website and updates and refreshes the league table for a particular team/season
    url(r'^(?P<slug>[-\w]+)/stats/(?P<season_pk>\d+)/ajax/scrape/$',
        views.ScrapeLeagueTableView.as_view(),
        name='refresh_league_table'),

)
