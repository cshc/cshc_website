import logging
from django.views.generic import DetailView, ListView
from braces.views import SelectRelatedMixin
from .models import TrainingSession

log = logging.getLogger(__name__)


class UpcomingTrainingSessionsView(ListView):
    """View for a list of upcoming training sessions"""

    model = TrainingSession

    # Only select the next four training sessions
    queryset = TrainingSession.objects.upcoming().select_related('venue')[:4]

    @staticmethod
    def add_upcoming_training_to_context(context):
        context['trainingsession_list'] = UpcomingTrainingSessionsView.queryset


class TrainingSessionDetailView(SelectRelatedMixin, DetailView):
    """View for the details of a training session"""
    model = TrainingSession
    select_related = ['venue']
