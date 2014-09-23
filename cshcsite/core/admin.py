from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from .forms import FlatPageForm, UserChangeForm, UserCreationForm, ZinniaEntryAdminForm
from .models import ClubInfo, ContactSubmission, CshcUser
from zinnia.models.entry import Entry
from zinnia.admin.entry import EntryAdmin

# Override the provided admin interface for blog entries - simplify it a bit
# and add support (via a custom form) for WYSIWYG entry
class ZinniaEntryAdmin(EntryAdmin):
    form = ZinniaEntryAdminForm

    fieldsets = (
        (_('Content'), {
            'fields': (('title', 'status'), 'content', 'image')}),
        (_('Publication'), {
            'fields': (('start_publication', 'end_publication'),
                       'creation_date'),
            'classes': ('collapse', 'collapse-closed')}),
        (_('Templates'), {
            'fields': ('content_template', 'detail_template'),
            'classes': ('collapse', 'collapse-closed')}),
        (None, {'fields': ('featured', 'comment_enabled', 'excerpt', 'authors', 'related', 'categories', 'tags', 'slug')}))


admin.site.unregister(Entry)
admin.site.register(Entry, ZinniaEntryAdmin)

class RedactorFlatPageAdmin(FlatPageAdmin):
    """Override for the FlatPage admin interface - uses a Redactor widget"""

    form = FlatPageForm
    fieldsets = [
        ('None', {'fields': ['url', 'title', 'sites']}),
        ('Advanced options', {'classes': ('collapse',), 'fields': ('enable_comments', 'registration_required', 'template_name')}),

        ('Content', {
            'classes': ('full-width',),
            'fields': ['content']}),
    ]


class ClubInfoAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')


class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'submitted')

###############################################################################
# USERS


class CshcUserAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')}),
    )
    search_fields = ('first_name', 'last_name', 'email')
    ordering = ('email',)
    filter_horizontal = ()


###############################################################################

# Re-register the FlatPage admin interface
admin.site.register(CshcUser, CshcUserAdmin)
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, RedactorFlatPageAdmin)
admin.site.register(ClubInfo, ClubInfoAdmin)
admin.site.register(ContactSubmission)
