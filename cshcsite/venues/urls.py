from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',

    # E.g. '/venues/'
    url(r'^/?$',
        views.VenueListView.as_view(), 
        name="venue_list"
    ),

    # E.g. '/venues/leys/'
    url(r'^(?P<slug>[-\w]+)/$',
        views.VenueDetailView.as_view(), 
        name="venue_detail"
    ),

)