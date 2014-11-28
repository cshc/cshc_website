""" URL routing related to venues.
"""

from django.conf.urls import patterns, url

from venues import views

urlpatterns = patterns('',

    # E.g. '/venues/'           - Lists all venues, home and away. Filterable.
    url(r'^/?$',
        views.VenueListView.as_view(),
        name="venue_list"
    ),

    # E.g. '/venues/leys/'      - Details on a particular venue.
    url(r'^(?P<slug>[-\w]+)/$',
        views.VenueDetailView.as_view(),
        name="venue_detail"
    ),

)
