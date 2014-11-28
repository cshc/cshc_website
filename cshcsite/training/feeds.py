""" Automatically generated calendar feed for training sessions.

    This feed can be added to an external calendar app to display all
    training sessions.

    Ref: http://django-ics.readthedocs.org/en/latest/usage.html#overview
"""

from django_ical.views import ICalFeed
from datetime import timedelta
from training.models import TrainingSession


class TrainingSessionICalFeed(ICalFeed):
    """
    The iCal calendar feed for training sessions.

    Provides a calendar feed of all training sessions for the current season.
    """
    product_id = '-//cambridgesouthhockeyclub.co.uk//Calendar 1.0//EN'
    timezone = 'Europe/London'
    item_class = 'PUBLIC'

    title = 'CSHC training sessions'
    description = "CSHC training sessions: up-to-date details of all training sessions for the current season"

    def items(self):
        """Gets all the training sesssions for the current season"""
        return TrainingSession.objects.this_season().select_related('venue')

    def item_title(self, item):
        """Gets the title of the training session.

        Note - this will include the status.
        """
        if item.status == TrainingSession.STATUS.Cancelled:
            return "CANCELLED: {}".format(item.description)
        return item.description

    def item_link(self, item):
        """Gets a link/url for the training session"""
        return item.get_absolute_url()

    def item_location(self, item):
        """Gets the location of the training session"""
        if item.venue_id is not None:
            return item.venue.full_address()
        else:
            return None

    def item_start_datetime(self, item):
        """Gets the start time of the training session"""
        return item.datetime

    def item_end_datetime(self, item):
        """Gets the end time of the training session"""
        return item.datetime + timedelta(minutes=item.duration_mins)
