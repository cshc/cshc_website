from django import forms
from django.forms.widgets import Textarea


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    subject = forms.CharField()
    message = forms.CharField(widget=Textarea())
