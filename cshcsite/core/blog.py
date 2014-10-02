from django import forms
from django.db.models import ManyToManyRel
from suit_redactor.widgets import RedactorWidget
from zinnia.models import Entry, Category
from zinnia.admin.forms import EntryAdminForm



# Override the provided form and add support for WYSIWYG entry.
# Also removed reference to unused field 'sites'
class ZinniaEntryAdminForm(EntryAdminForm):
    def __init__(self, *args, **kwargs):
        forms.ModelForm.__init__(self, *args, **kwargs)
        rel = ManyToManyRel(Category, 'id')
        self.fields['categories'].widget = RelatedFieldWidgetWrapper(
            self.fields['categories'].widget, rel, self.admin_site)

    class Meta:
        model = Entry
        fields = forms.ALL_FIELDS
        widgets = {
            'content': RedactorWidget(editor_options={'lang': 'en', 'minHeight': 400}),
            'excerpt': RedactorWidget(editor_options={'lang': 'en', 'minHeight': 200})
        }

