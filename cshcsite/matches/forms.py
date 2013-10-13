from django import forms
from .models import Match
from suit_redactor.widgets import RedactorWidget


class MatchForm(forms.ModelForm):
    """
    A form for entering match details.
    A TinyMCE widget is specified for editing the Pre-Match Hype and Report Body fields.
    """
    class Meta:
        model = Match
        widgets = {
            'pre_match_hype': RedactorWidget(editor_options={'lang': 'en', 'minHeight': 150}),
            'report_body': RedactorWidget(editor_options={'lang': 'en', 'minHeight': 400})
        }