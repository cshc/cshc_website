from django import forms
from django.contrib.flatpages.models import FlatPage
from tinymce.widgets import TinyMCE
from .models import ContactSubmission


class FlatPageForm(forms.ModelForm):
    """Form for the FlatPage model - uses a TinyMCE widget"""
    class Meta:
        model = FlatPage
        widgets = {
            'content': TinyMCE(attrs={'rows': 50}, mce_attrs={'width': '100%', 'plugin_preview_pageurl': '/tinymce/preview/flatpages/'}),
        }


class ContactSubmissionForm(forms.ModelForm):
    """Form used for the contact form"""

    class Meta:
        model = ContactSubmission
        # our_notes is only to be used by staff/admin
        exclude = ('our_notes',)
