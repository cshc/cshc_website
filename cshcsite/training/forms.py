""" Custom forms related to training sessions.
"""

import logging
from datetime import timedelta, datetime
from django import forms
from training.models import TrainingSession
from venues.models import Venue

LOG = logging.getLogger(__name__)

MULTIPLE = 'M'
UNTIL = 'U'
REPEAT_CHOICES = (
    (MULTIPLE, "Multiple"),
    (UNTIL, "Until")
)

DATE_INPUT_FORMATS = ['%Y-%m-%d', '%d/%m/%Y', '%d-%m-%Y', '%d/%m/%y', '%d-%m-%y']
TIME_INPUT_FORMATS = ['%H:%M']

class TrainingSessionForm(forms.Form):
    """ A custom form for adding multiple training sessions. """
    venue = forms.ModelChoiceField(queryset=Venue.objects.home_venues())
    description = forms.CharField(min_length=2, max_length=200)
    duration_mins = forms.IntegerField(min_value=10, max_value=480, initial=90)  # Prevent silly numbers
    datetime = forms.SplitDateTimeField(input_date_formats=DATE_INPUT_FORMATS,
                                        input_time_formats=TIME_INPUT_FORMATS, initial=datetime.now())
    repeat = forms.BooleanField(initial=True, required=False)
    repeat_option = forms.ChoiceField(choices=REPEAT_CHOICES,
                                      widget=forms.RadioSelect)
    repeat_count = forms.IntegerField(min_value=2, max_value=52, initial=10, required=False)
    repeat_until = forms.DateField(input_formats=DATE_INPUT_FORMATS, required=False)

    def save_training_sessions(self):
        """ Save the training sessions specified by the form data. """
        print self.cleaned_data
        if self.cleaned_data['repeat']:
            # Save multiple training sessions
            sessions = []
            if self.cleaned_data['repeat_option'] == MULTIPLE:
                LOG.info("Saving {} repeated training sessions".format(self.cleaned_data['repeat_count']))
                for i in range(0, self.cleaned_data['repeat_count']):
                    sessions.append(self.new_session(i))
            else:
                LOG.info("Saving repeated training sessions up to {}".format(self.cleaned_data['repeat_until']))
                week_offset = 0
                start_date = self.cleaned_data['datetime'].date()
                end = self.cleaned_data['repeat_until']
                while end > (start_date + timedelta(days=week_offset*7)):
                    sessions.append(self.new_session(week_offset))
                    week_offset += 1
            return sessions

        else:
            LOG.info("Saving a single training session")
            return [self.new_session(0)]


    def new_session(self, week_offset):
        """ Adds a new training session at the specified week offset. """
        session = TrainingSession()
        session.venue = self.cleaned_data['venue']
        session.description = self.cleaned_data['description']
        session.datetime = self.cleaned_data['datetime'] + timedelta(days=week_offset*7)
        session.duration_mins = self.cleaned_data['duration_mins']
        session.save()
        return session

    # class Meta:
    #     """ Meta-info for the form. """
    #     model = TrainingSession
    #     widgets = {
    #         'datetime': DateTimeWidget(attrs={'id':"id_datetime"}, bootstrap_version=2)
    #     }

