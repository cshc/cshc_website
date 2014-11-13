import logging
from django.utils import timezone
from django.db import models
from django.db.models.query import QuerySet
from datetime import datetime
from model_utils import Choices
from model_utils.managers import PassThroughManager
from model_utils.fields import StatusField
from venues.models import Venue
from competitions.models import Season

log = logging.getLogger(__name__)


class TrainingSessionQuerySet(QuerySet):
    """Common queries relating to the TrainingSession model"""

    def upcoming(self):
        """Returns only training sessions in the future, sorted by date"""
        return self.filter(datetime__gte=timezone.now()).order_by('datetime')

    def before(self, dt):
        return self.filter(datetime__lt=dt).order_by('datetime')

    def this_season(self):
        """Returns only training sessions for this season"""
        season = Season.current()
        return self.filter(datetime__gte=season.start, datetime__lte=season.end).order_by('datetime')


class TrainingSession(models.Model):
    """Represents a training session"""

    STATUS = Choices('Scheduled', 'Cancelled')

    venue = models.ForeignKey(Venue)
    """The venue where the training session takes place"""

    description = models.CharField(max_length=100, default='Full club training')
    """The type of training session"""

    datetime = models.DateTimeField("Training date/time")
    """The start time (and date) of the training session"""

    duration_mins = models.PositiveSmallIntegerField("Duration (minutes)", default=120)
    """The duration, in minutes, of the training session"""

    status = StatusField()
    """The status of the training session (e.g. cancelled/scheduled)"""

    objects = PassThroughManager.for_queryset_class(TrainingSessionQuerySet)()

    class Meta:
        app_label = 'training'
        ordering = ['datetime']
        unique_together = ('description', 'datetime')

    def __unicode__(self):
        return "{} ({})".format(self.description, self.datetime)

    @models.permalink
    def get_absolute_url(self):
        return ('trainingsession_detail', [self.pk])
