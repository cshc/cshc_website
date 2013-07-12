from django import forms
from tinymce.widgets import TinyMCE
from .models import Match


class MatchForm(forms.ModelForm):
    """
    A form for entering match details.
    A TinyMCE widget is specified for editing the Pre-Match Hype and Report Body fields.
    """
    class Meta:
        model = Match
        widgets = {
            'pre_match_hype': TinyMCE(attrs={'rows': 5}, mce_attrs={'width':'100%', 'plugin_preview_pageurl': '/tinymce/preview/pre_match_hype/'}),
            'report_body': TinyMCE(attrs={'rows': 30}, mce_attrs={'width':'100%', 'plugin_preview_pageurl': '/tinymce/preview/match_report/'}),
        }