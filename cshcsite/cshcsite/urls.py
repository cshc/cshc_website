""" The starting point for URL routing for the whole CSHC site.

    URL routing for other apps are delegated from here using the
    'include' call.
"""

from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
from venues.views import HomeVenueListView
from core.views import ContactSubmissionCreateView, RegistrationView
from members.views import ProfileView
from .sitemap import CshcSitemap
from . import views

# Automatically load the INSTALLED_APPS admin.py modules.
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^$', views.HomeView.as_view(), name='homepage'),                                              # The main landing page

    url(r'^about/$',                  TemplateView.as_view(template_name='core/about_us.html'), name='about_us'),                                     # About Us
    url(r'^calendar/$',               views.CalendarView.as_view(),  name='calendar'),
    url(r'^contact/$',                ContactSubmissionCreateView.as_view(),  name='contact_us'),
    url(r'^commission/$',             TemplateView.as_view(template_name='core/commission.html'),  name='commission'),
    url(r'^offers/$',                 TemplateView.as_view(template_name='core/offers.html'),  name='members_offers'),

    url(r'^about/directions/$',       HomeVenueListView.as_view(), name='directions'),            # Directions - basically a list of home venues
    url(r'^about/social/$',           TemplateView.as_view(template_name='core/social.html'), name='about_social'),
    url(r'^about/kit/$',              TemplateView.as_view(template_name='core/kit.html'), name='about_kit'),
    url(r'^about/fees/$',             views.FeesView.as_view(), name='about_fees'),

    url(r'^about/committee/$',        views.CommitteeSeasonView.as_view(), name="about_committee"),
    # E.g. '/about/committee/2011-2012/'
    url(r'^about/committee/(?P<season_slug>[-\w]+)/$',
        views.CommitteeSeasonView.as_view(),
        name="about_committee_season"
    ),

    url(r'^stats/$',                  TemplateView.as_view(template_name='core/stats.html'), name='stats'),

    url(r'^archive/minutes/$',         TemplateView.as_view(template_name='core/meeting_minutes.html'), name='about_minutes'),
    url(r'^archive/chairmans-notes/$', TemplateView.as_view(template_name='core/chairmans_notes.html'), name='chairmans_notes'),
    url(r'^archive/social/dinner2014/$', TemplateView.as_view(template_name='core/social/dinner2014.html'), name='dinner2014'),
    url(r'^archive/social/dinner2013/$', TemplateView.as_view(template_name='core/social/dinner2013.html'), name='dinner2013'),
    url(r'^archive/social/dinner2012/$', TemplateView.as_view(template_name='core/social/dinner2012.html'), name='dinner2012'),
    url(r'^archive/social/dinner2011/$', TemplateView.as_view(template_name='core/social/dinner2011.html'), name='dinner2011'),
    url(r'^archive/social/dinner2010/$', TemplateView.as_view(template_name='core/social/dinner2010.html'), name='dinner2010'),
    url(r'^archive/social/dinner2009/$', TemplateView.as_view(template_name='core/social/dinner2009.html'), name='dinner2009'),
    url(r'^archive/social/dinner2008/$', TemplateView.as_view(template_name='core/social/dinner2008.html'), name='dinner2008'),
    url(r'^archive/social/dinner2007/$', TemplateView.as_view(template_name='core/social/dinner2007.html'), name='dinner2007'),
    url(r'^archive/social/tour2008/$', TemplateView.as_view(template_name='core/social/tour2008.html'), name='tour2008'),


    # Delegate to apps
    url(r'^matches/', include('matches.urls')),
    url(r'^members/', include('members.urls')),
    url(r'^opposition/', include('opposition.urls')),
    url(r'^teams/', include('teams.urls')),
    url(r'^venues/', include('venues.urls')),
    url(r'^training/', include('training.urls')),

    url(r'^accounts/profile/$', ProfileView.as_view(), name='user_profile'),
    url(r'^accounts/register/$', RegistrationView.as_view(), name='registration_register'),
    url(r'^accounts/', include('registration.backends.default.urls')),

    # WYSIWYG editor urls (used for image and file uploads)
    url(r'^redactor/', include('redactor.urls')),

    # Zinnia blog
    # Ref: http://docs.django-blog-zinnia.com/
    url(r'^blog/', include('zinnia.urls', namespace="zinnia")),

    url(r'^admin/', include(admin.site.urls)),

    # Redirects from the old website
    url(r'^pages/', include('core.redirect_urls')),

    # Sitemap (indexed)
    url(r'^sitemap\.xml$', 'django.contrib.sitemaps.views.index', {'sitemaps': CshcSitemap}),
    url(r'^sitemap-(?P<section>.+)\.xml$', 'django.contrib.sitemaps.views.sitemap', {'sitemaps': CshcSitemap}),
)

# Static pages - use the flatpage app
urlpatterns += patterns('django.contrib.flatpages.views',
    (r'^(?P<url>.*/)$', 'flatpage'),
)


# DEBUG only: Add the media folder to the static pages urls
# Ref: http://stackoverflow.com/a/5518073
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
