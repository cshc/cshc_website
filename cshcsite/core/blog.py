""" Classes relating to the Zinnia blog app. Encapsulated here in one module.
"""

from django import forms
from django.db.models import ManyToManyRel
from django.contrib.sites.models import Site
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from redactor.widgets import RedactorEditor
from zinnia.models import Entry, Category
from zinnia.admin.forms import EntryAdminForm, CategoryAdminForm


BLOG_UPLOAD_DIR = "uploads/blog/"


class ZinniaEntryAdminForm(EntryAdminForm):
    """ Overrides the default admin form, adding a couple of redactor
        editor widget.
    """

    class Meta:
        """ Meta-info for the form. """
        model = Entry
        fields = forms.ALL_FIELDS
        widgets = {
            'content': RedactorEditor(upload_to=BLOG_UPLOAD_DIR,
                                      redactor_options={'minHeight': 400}),
            'excerpt': RedactorEditor(upload_to=BLOG_UPLOAD_DIR,
                                      redactor_options={'minHeight': 200})
        }


class ZinniaCategoryAdminForm(CategoryAdminForm):
    """ Overrides the default admin form, adding a redactor editor widget. """

    class Meta:
        """ Meta-info for the form. """
        model = Category
        fields = forms.ALL_FIELDS
        widgets = {
            'description': RedactorEditor(upload_to=BLOG_UPLOAD_DIR,
                                          redactor_options={'minHeight': 200})
        }
