from django import forms
from django.core.urlresolvers import reverse
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE


class FlatPageForm(forms.ModelForm):
    """Form for the FlatPage model - uses a TinyMCE widget"""
    class Meta:
        model = FlatPage
        widgets = {
            'content': TinyMCE(attrs={'rows': 50}, mce_attrs={'width':'100%', 'plugin_preview_pageurl': '/tinymce/preview/flatpages/'}),
        }