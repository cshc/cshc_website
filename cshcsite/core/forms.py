""" Various Django forms:

    FlatPageForm - for creating/updating flat pages.
    ContactSubmissionForm - for submitting 'Contact Us' form
    JuniorsContactSubmissionForm - for submitting an enquery about juniors
    UserCreationForm - creating new users
    UserChangeForm - used for changing user's password
"""

from django import forms
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from redactor.widgets import RedactorEditor
from core.models import ContactSubmission, CshcUser, JuniorsContactSubmission


class FlatPageForm(forms.ModelForm):
    """ Form for the FlatPage model - uses a Redactor widget"""

    class Meta:
        """ Meta-info for the form. """
        model = FlatPage
        widgets = {
            'content': RedactorEditor(upload_to="uploads/flatpages/",
                                      redactor_options={'minHeight': 400}),
        }


class ContactSubmissionForm(forms.ModelForm):
    """ Form used for the contact form"""

    class Meta:
        """ Meta-info for the form. """
        model = ContactSubmission
        # our_notes is only to be used by staff/admin
        exclude = ('our_notes',)


class JuniorsContactSubmissionForm(forms.ModelForm):
    """ Form used for the contact form"""

    class Meta:
        """ Meta-info for the form. """
        model = JuniorsContactSubmission
        # our_notes is only to be used by staff/admin
        exclude = ('our_notes',)


class UserCreationForm(forms.ModelForm):
    """ A form that creates a user, with no privileges, from the given email and
        password.
    """
    error_messages = {
        'duplicate_email': "A user with that email address already exists.",
        'password_mismatch': "The two password fields didn't match.",
    }

    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Password confirmation",
                                widget=forms.PasswordInput,
                                help_text="Enter the same password as above, for verification.")

    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields['first_name'].required = True
        self.fields['last_name'].required = True

    class Meta:
        """ Meta-info for the form. """
        model = CshcUser
        fields = ('email', 'first_name', 'last_name')

    def clean_email(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        email = self.cleaned_data["email"]
        try:
            CshcUser.objects.get(email=email)
        except CshcUser.DoesNotExist:
            return email
        raise forms.ValidationError(self.error_messages['duplicate_email'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """ Used for changing the user's password. """

    password = ReadOnlyPasswordHashField(label="Password",
        help_text="Raw passwords are not stored, so there is no way to see "
                  "this user's password, but you can change the password "
                  "using <a href=\"password/\">this form</a>.")

    class Meta:
        """ Meta-info for the form. """
        model = CshcUser

    def __init__(self, *args, **kwargs):
        super(UserChangeForm, self).__init__(*args, **kwargs)
        permissions = self.fields.get('user_permissions', None)
        if permissions is not None:
            permissions.queryset = permissions.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]
