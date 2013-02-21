from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'club.views.index'),
    
    # Matches
    url(r'^matches/(\d+)$', 'club.views.matches.details'),
    
    url(r'^admin/', include(admin.site.urls)),
)
