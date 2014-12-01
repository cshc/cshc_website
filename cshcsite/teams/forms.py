""" Custom forms for the Teams models
"""

from django import forms
from redactor.widgets import RedactorEditor
from teams.models import ClubTeamSeasonParticipation


class ClubTeamSeasonParticipationForm(forms.ModelForm):
    """ A form for entering Club Team Season Participation details.
        A Redactor widget is specified for editing the blurb and team_photo_caption fields.
    """
    class Meta:
        """ Meta-info for the form. """
        model = ClubTeamSeasonParticipation
        widgets = {
            'blurb': RedactorEditor(redactor_options={'minHeight': 150}),
            'team_photo_caption': RedactorEditor(redactor_options={'minHeight': 150}),
        }
