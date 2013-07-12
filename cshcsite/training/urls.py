from django.conf.urls import patterns, url

from . import views, feeds

urlpatterns = patterns('',

    # E.g. '/training/'
    url(r'^$',
        views.UpcomingTrainingSessionsView.as_view(), 
        name="upcoming_trainingsession_list"
    ),

    # E.g. '/training/41/'
    url(r'^(?P<pk>\d+)/$',
        views.TrainingSessionDetailView.as_view(), 
        name="trainingsession_detail"
    ),

    # E.g. '/training/cshc_training.ics'
    url(r'^cshc_training.ics$',
        feeds.TrainingSessionICalFeed(), 
        name="trainingsession_ical_feed"
    ),
)