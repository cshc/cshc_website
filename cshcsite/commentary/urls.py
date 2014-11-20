from django.conf.urls import patterns, url
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = patterns('',

    # REST API for match comments
    # (the ordering of these urls is important)
    url(r'^(?P<match_id>\d+)/since/(?P<last_update>\d+)/$',
        views.MatchCommentList.as_view(),
        name="latest_match_comments"
    ),

    url(r'^(?P<match_id>\d+)/(?P<pk>\d+)/$',
        views.MatchCommentDetail.as_view(),
        name="match_comment_detail"
    ),

    url(r'^(?P<match_id>\d+)/$',
        views.MatchCommentList.as_view(),
        name="latest_match_comments_default"
    ),
)

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
