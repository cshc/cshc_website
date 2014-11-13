from django import forms
from .models import ClubTeamSeasonParticipation
from redactor.widgets import RedactorEditor


class ClubTeamSeasonParticipationForm(forms.ModelForm):
    """
    A form for entering Club Team Season Participation details.
    A TinyMCE widget is specified for editing the blurb and team_photo_caption fields.
    """
    class Meta:
        model = ClubTeamSeasonParticipation
        widgets = {
            'blurb': RedactorEditor(redactor_options={'minHeight': 150}),
            'team_photo_caption': RedactorEditor(redactor_options={'minHeight': 150}),
        }