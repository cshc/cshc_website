from django.conf.urls import patterns, include, url
from django.views.generic import RedirectView
from django.views.generic import TemplateView
from django.contrib import admin
from django.conf import settings
from venues.views import HomeVenueListView
from . import views

admin.autodiscover()

urlpatterns = patterns('',
    
    url(r'^$', views.HomeView.as_view(), name='homepage'),                                              # The main landing page
    url(r'^about/$', views.AboutUsView.as_view(), name='about_us'),                                     # About Us

    url(r'^calendar/$',               TemplateView.as_view(template_name='core/calendar.html'),  name='calendar'),
    url(r'^contact/$',                views.ContactUsView.as_view(),  name='contact_us'),
    url(r'^commission/$',             TemplateView.as_view(template_name='core/commission.html'),  name='commission'),
    url(r'^offers/$',                 TemplateView.as_view(template_name='core/offers.html'),  name='members_offers'),
    
    url(r'^about/pitch-directions/$', HomeVenueListView.as_view(), name='pitch_directions'),            # Pitch directions - basically a list of home venues
    url(r'^about/social/$',           TemplateView.as_view(template_name='core/social.html'), name='about_social'),
    url(r'^about/kit/$',              TemplateView.as_view(template_name='core/kit.html'), name='about_kit'),
    url(r'^about/fees/$',             TemplateView.as_view(template_name='core/fees.html'), name='about_fees'),
    url(r'^about/committee/$',        views.CommitteeView.as_view(), name='about_committee'),
    
    url(r'^archive/minutes/$',         TemplateView.as_view(template_name='core/meeting_minutes.html'), name='about_minutes'),
    url(r'^archive/chairmans-notes/$', TemplateView.as_view(template_name='core/chairmans_notes.html'), name='chairmans_notes'),
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

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/data-migration/', views.DataMigrationAdminView.as_view(), name='data_migration'),
    url(r'^admin/', include(admin.site.urls)),

    # TinyMCE
    url(r'^tinymce/', include('tinymce.urls')),                                                         # Used for editor previews etc

    # Redirects/aliases
    url(r'^join-us/$', RedirectView.as_view(url='/members/enquiries/new/'), name='join_us'),            # Membership enquiry form

    # Ajax views
    url(r'^load-tweets/$', views.LoadTweetsView.as_view(), name='load_tweets_url'),
)

# Static pages - use the flatpage app
urlpatterns += patterns('django.contrib.flatpages.views',
    url(r'^members-offers/$',       'flatpage', {'url': '/members-offers/'},    name='members_offers'),
    url(r'^commission/$',           'flatpage', {'url': '/commission/'},        name='commission'),
    
)


# DEBUG only: Add the media folder to the static pages urls
# Ref: http://stackoverflow.com/a/5518073
if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}))
