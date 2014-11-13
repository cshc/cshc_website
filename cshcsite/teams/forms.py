from django import forms
from .models import ClubTeamSeasonParticipation
from suit_redactor.widgets import RedactorWidget


class ClubTeamSeasonParticipationForm(forms.ModelForm):
    """
    A form for entering Club Team Season Participation details.
    A TinyMCE widget is specified for editing the blurb and team_photo_caption fields.
    """
    class Meta:
        model = ClubTeamSeasonParticipation
        widgets = {
            'blurb': RedactorWidget(editor_options={'lang': 'en', 'minHeight': 150}),
            'team_photo_caption': RedactorWidget(editor_options={'lang': 'en', 'minHeight': 150}),
        }