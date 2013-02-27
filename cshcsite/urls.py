from django.conf.urls import patterns, include, url
from club import urls;

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += urls.club_urlpatterns;
