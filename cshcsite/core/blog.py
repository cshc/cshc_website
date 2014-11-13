from django import forms
from django.db.models import ManyToManyRel
from django.contrib.sites.models import Site
from django.contrib.admin.widgets import RelatedFieldWidgetWrapper
from redactor.widgets import RedactorEditor
from zinnia.models import Entry, Category
from zinnia.admin.forms import EntryAdminForm, CategoryAdminForm


# Override the provided form and add support for WYSIWYG entry.
# Also removed reference to unused field 'sites'
class ZinniaEntryAdminForm(EntryAdminForm):
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        rel = ManyToManyRel(Category, 'id')
        self.fields['sites'].initial = [Site.objects.get_current()]
        self.fields['categories'].widget = RelatedFieldWidgetWrapper(
            self.fields['categories'].widget, rel, self.admin_site)

    class Meta:
        model = Entry
        fields = forms.ALL_FIELDS
        widgets = {
            'content': RedactorEditor(upload_to="uploads/blog/", redactor_options={'minHeight': 400}),
            'excerpt': RedactorEditor(upload_to="uploads/blog/", redactor_options={'minHeight': 200})
        }

class ZinniaCategoryAdminForm(CategoryAdminForm):
    class Meta:
        model = Category
        fields = forms.ALL_FIELDS
        widgets = {
            'description': RedactorEditor(upload_to="uploads/blog/", redactor_options={'minHeight': 200})
        }