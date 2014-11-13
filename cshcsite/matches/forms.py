from django import forms
from .models import Match
from redactor.widgets import RedactorEditor

class MatchForm(forms.ModelForm):
    """
    A form for entering match details.
    A TinyMCE widget is specified for editing the Pre-Match Hype and Report Body fields.
    """
    class Meta:
        model = Match
        widgets = {
            'pre_match_hype': RedactorEditor(upload_to="uploads/match_reports/", redactor_options={'minHeight': 150}),
            'report_body': RedactorEditor(upload_to="uploads/match_reports/", redactor_options={'minHeight': 400})
        }