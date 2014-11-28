""" URL routing related to training sessions."""

from django.conf.urls import patterns, url
from training import views, feeds

urlpatterns = patterns('',

    # E.g. '/training/'                     - Lists all upcoming training sessions
    url(r'^$',
        views.UpcomingTrainingSessionsView.as_view(),
        name="upcoming_trainingsession_list"
    ),

    # E.g. '/training/41/'                  - Details of a particular training session
    url(r'^(?P<pk>\d+)/$',
        views.TrainingSessionDetailView.as_view(),
        name="trainingsession_detail"
    ),

    # E.g. '/training/cshc_training.ics'    - Automatically generated ical calendar feed of training sessions
    url(r'^cshc_training.ics$',
        feeds.TrainingSessionICalFeed(),
        name="trainingsession_ical_feed"
    ),
)
