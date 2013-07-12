from django import forms
from .models import Member, MembershipEnquiry


class MembershipEnquiryForm(forms.ModelForm):
    """Form used for membership enquiries"""

    class Meta:
        model = MembershipEnquiry
        # our_notes is only to be used by staff/admin
        exclude = ('our_notes',)