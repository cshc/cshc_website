""" Custom forms relating to matches.
"""

from django import forms
from redactor.widgets import RedactorEditor
from matches.models import Match

class MatchForm(forms.ModelForm):
    """ A form for entering match details.
        A Redactor widget is specified for editing the Pre-Match Hype
        and Report Body fields.

        Ref: https://github.com/TigorC/django-redactorjs
    """
    class Meta:
        """ Meta-info for the form."""
        model = Match
        widgets = {
            'pre_match_hype': RedactorEditor(upload_to="uploads/match_reports/",
                                             redactor_options={'minHeight': 150}),
            'report_body': RedactorEditor(upload_to="uploads/match_reports/",
                                          redactor_options={'minHeight': 400})
        }
