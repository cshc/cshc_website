from django.conf.urls import patterns, url
from core.views import RegisterUserView
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

    # Ajax requests
    # E.g. '/members/23/ajax/stats/'
    url(r'^(?P<pk>\d+)/ajax/stats/$', views.MemberStatsView.as_view(), name='member_stats_ajax'),

    # Accounts. Ref: https://github.com/django/django/blob/master/django/contrib/auth/urls.py
    url(r'^register/$', RegisterUserView.as_view(), name='register'),
    #url(r'^login/$', views.login, kwargs={'SSL':True}, name='login'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', name='logout'),
    url(r'^password-change/$', 'django.contrib.auth.views.password_change', name='password_change'),
    url(r'^password-change/done/$', 'django.contrib.auth.views.password_change_done', name='password_change_done'),
    url(r'^password-reset/$', 'django.contrib.auth.views.password_reset', name='password_reset'),
    url(r'^password-reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', name='password_reset_complete'),
    url(r'^reset/(?P<uidb36>[0-9A-Za-z]{1,13})-(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', 'django.contrib.auth.views.password_reset_confirm', name='password_reset_confirm'),
    url(r'^profile/$', views.ProfileView.as_view(), name='user_profile'),
)
