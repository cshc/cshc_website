from django.conf.urls import patterns, url
from competitions.models import Season
from . import views, feeds

urlpatterns = patterns('',

    # E.g. '/matches/'
    url(r'^$',
        views.MatchListView.as_view(),
        name="match_list"
    ),

    # E.g. '/matches/23/'
    url(r'^(?P<pk>\d+)/$',
        views.MatchDetailView.as_view(),
        name="match_detail"
    ),

    # E.g. '/matches/23-Apr-13/'
    url(r'^(?P<date>\d{2}-[a-zA-Z]{3}-\d{2})/$',
        views.MatchesByDateView.as_view(),
        name="matches_by_date"
    ),

    # E.g. '/matches/by-season/'
    url(r'^by-season/$',
        views.MatchesBySeasonView.as_view(),
        name="matches_by_season_default"
    ),

    # E.g. '/matches/by-season/2011-2012/'
    url(r'^by-season/(?P<season_slug>[-\w]+)/$',
        views.MatchesBySeasonView.as_view(),
        name="matches_by_season"
    ),


    # E.g. '/matches/latest-results/'
    url(r'^latest-results/$',
        views.LatestResultsView.as_view(),
        name="latest_results"
    ),

    # E.g. '/matches/next-fixtures/'
    url(r'^next-fixtures/$',
        views.NextFixturesView.as_view(),
        name="next_fixtures"
    ),

    # E.g. '/matches/goal-king/'
    url(r'^goal-king/$',
        views.GoalKingSeasonView.as_view(),
        name="goal_king"
    ),

    # E.g. '/matches/goal-king/2011-2012/'
    url(r'^goal-king/(?P<season_slug>[-\w]+)/$',
        views.GoalKingSeasonView.as_view(),
        name="goal_king_season"
    ),

    # E.g. '/matches/goal-king/2011-2012/ajax/'
    url(r'^goal-king/(?P<season_slug>[-\w]+)/ajax/$',
        views.GoalKingSeasonUpdateView.as_view(),
        name="goal_king_season_update"
    ),

    # E.g. '/matches/accidental-tourist/'
    url(r'^accidental-tourist/$',
        views.AccidentalTouristSeasonView.as_view(),
        name="accidental_tourist"
    ),

    # E.g. '/matches/accidental-tourist/2011-2012/'
    url(r'^accidental-tourist/(?P<season_slug>[-\w]+)/$',
        views.AccidentalTouristSeasonView.as_view(),
        name="accidental_tourist_season"
    ),

    # E.g. '/matches/accidental-tourist/2011-2012/ajax/'
    url(r'^accidental-tourist/(?P<season_slug>[-\w]+)/ajax/$',
        views.AccidentalTouristSeasonUpdateView.as_view(),
        name="accidental_tourist_season_update"
    ),

    # E.g. '/matches/naughty-step/'
    url(r'^naughty-step/$',
        views.NaughtyStepView.as_view(),
        name="naughty_step"
    ),

    # Feeds
    url(r'^feed/rss/$',                          # RSS feed of match reports
        feeds.RssMatchReportsFeed(),
        name="match_report_rss_feed"
    ),
    url(r'feed/atom/$',                         # Atom feed of match reports
        feeds.AtomMatchReportsFeed(),
        name="match_report_atom_feed"
    ),
    # E.g. '/matches/cshc_matches.ics'
    url(r'^cshc_matches.ics$',
        feeds.MatchICalFeed(),
        name="match_ical_feed"
    ),
)