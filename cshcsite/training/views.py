""" Django Views related to training sessions.
"""

from django.views.generic import DetailView, ListView
from braces.views import SelectRelatedMixin
from training.models import TrainingSession


# The max number of upcoming training sessions to display
MAX_SESSIONS_TO_DISPLAY = 5


class UpcomingTrainingSessionsView(ListView):
    """View for a list of upcoming training sessions"""

    model = TrainingSession

    queryset = TrainingSession.objects.upcoming().select_related('venue')[:MAX_SESSIONS_TO_DISPLAY]

    @staticmethod
    def add_upcoming_training_to_context(context):
        """ Utility method to add upcoming training session data to the
            given context. Useful when embedding a list of upcoming training
            sessions on other pages.
        """
        context['trainingsession_list'] = UpcomingTrainingSessionsView.queryset


class TrainingSessionDetailView(SelectRelatedMixin, DetailView):
    """View for the details of a training session"""
    model = TrainingSession
    select_related = ['venue']
