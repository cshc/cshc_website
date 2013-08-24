from django import forms
from .models import Member


class ProfileEditForm(forms.ModelForm):
    """Form used to edit your own profile"""

    class Meta:
        model = Member
        # our_notes is only to be used by staff/admin
        exclude = ('first_name', 'last_name', 'gender', 'is_current', 'user')

