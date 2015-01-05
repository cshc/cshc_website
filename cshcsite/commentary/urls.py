from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = patterns('',

    # REST API for match comments
    # (the ordering of these urls is important)

    url(r'^comments/(?P<match_id>\d+)/(?P<pk>\d+)/$',
        views.MatchCommentDetail.as_view(),
        name="match_comment_detail"
    ),

    url(r'^comments/(?P<match_id>\d+)/$',
        views.MatchCommentList.as_view(),
        name="match_comment_list"
    ),

    url(r'^commentators/(?P<match_id>\d+)/(?P<pk>\d+)/$',
        views.MatchCommentatorDetail.as_view(),
        name="match_commentator_detail"
    ),

    url(r'^commentators/(?P<match_id>\d+)/$',
        views.MatchCommentatorList.as_view(),
        name="match_commentator_list"
    ),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
