""" Custom forms for the Teams models
"""

from django import forms
from redactor.widgets import RedactorEditor
from teams.models import ClubTeamSeasonParticipation, TEAM_PHOTO_DIR


class ClubTeamSeasonParticipationForm(forms.ModelForm):
    """ A form for entering Club Team Season Participation details.
        A Redactor widget is specified for editing the blurb and team_photo_caption fields.
    """
    class Meta:
        """ Meta-info for the form. """
        model = ClubTeamSeasonParticipation
        widgets = {
            'blurb': RedactorEditor(upload_to=TEAM_PHOTO_DIR,
                                    redactor_options={'minHeight': 150}),
            'team_photo_caption': RedactorEditor(upload_to=TEAM_PHOTO_DIR,
                                                 redactor_options={'minHeight': 150}),
        }
