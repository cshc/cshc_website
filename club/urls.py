from django.conf.urls import patterns, include, url

club_urlpatterns = patterns('club.views',
    url(r'^$',             'static.index'),

    # Matches
    url(r'^matches/$',                                      'matches.index'),               # Main landing page for matches
    url(r'^matches/(\d+)$',                                 'matches.details'),             # Details of a particular match
    url(r'^matches/([a-z]+)-([a-z0-9]+)$',                  'matches.by_team'),             # Team fixtures/results (current season) 
    url(r'^matches/(\d{4})-\d{4}/([a-z0-9]+)-([a-z0-9]+)$', 'matches.by_season_and_team'),  # Team fixtures/results (particular season)
    url(r'^matches/(\d{4})-\d{4}$',                         'matches.by_season'),           # Season summary of matches
    url(r'^matches/(\d{2}-[a-zA-Z]{3}-\d{4})$',             'matches.by_date'),             # Summary of matches on a particular date

    # Venues
    url(r'^venues/$',                                       'venues.index'),                # Main landing page for venues
    url(r'^venues/(.+)$',                                   'venues.details'),              # Details of a venue

    # Teams
    url(r'^teams/$',                                       'teams.index'),                  # Main landing page for teams
    url(r'^teams/([a-z]+)-([a-z0-9]+)$',                   'teams.details'),                # Details of a team

    # Calendar
    url(r'^calendar/$',                                       'calendar.index'),                  # Main calendar
)