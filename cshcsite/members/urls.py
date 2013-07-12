from django.conf.urls import patterns, url
from django.views.generic import TemplateView

from . import views

urlpatterns = patterns('',

    # E.g. '/members/'
    url(r'^$',
        views.MemberListView.as_view(), 
        name="member_list"
    ),
    
    # E.g. '/members/32/'
    url(r'^(?P<pk>\d+)/$',
        views.MemberDetailView.as_view(), 
        name="member_detail"
    ),


    # E.g. '/members/enquiries/5/'
    url(r'^enquiries/(?P<pk>\d+)/$',
        views.MembershipEnquiryDetailView.as_view(), 
        name="membershipenquiry_detail"
    ),

    # E.g. '/members/enquiries/'
    url(r'^enquiries/$',
        views.MembershipEnquiryListView.as_view(), 
        name="membershipenquiry_list"
    ),

    # E.g. '/members/enquiries/new/'
    url(r'^enquiries/new/$',
        views.MembershipEnquiryCreateView.as_view(), 
        name="membershipenquiry_create"
    ),

    # Ajax requests
    # E.g. '/members/23/ajax/stats/'
    url(r'^(?P<pk>\d+)/ajax/stats/$', views.MemberStatsView.as_view(), name='member_stats_ajax'),

    # Accounts. Ref: https://github.com/django/django/blob/master/django/contrib/auth/urls.py
    url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^password-change/$', 'django.contrib.auth.views.password_change', name='password_change'),
    url(r'^password-change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'^password-reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^password-reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^profile/$', TemplateView.as_view(template_name='registration/profile.html'), name='user_profile'),
)