""" Configuration of Core models for the admin interface.
"""

from django.contrib import admin
from django.contrib.flatpages.admin import FlatPageAdmin
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from zinnia.models import Entry, Category
from zinnia.admin import EntryAdmin, CategoryAdmin
from core.forms import FlatPageForm, UserChangeForm, UserCreationForm
from core.models import ClubInfo, ContactSubmission, CshcUser, JuniorsContactSubmission
from core.blog import ZinniaEntryAdminForm, ZinniaCategoryAdminForm


class ZinniaEntryAdmin(EntryAdmin):
    """ Override the provided admin interface for blog entries - simplify it a bit
        and add support (via a custom form) for WYSIWYG entry.
    """
    form = ZinniaEntryAdminForm

    fieldsets = (
        (_('Content'), {
            'fields': (('title', 'status'), 'content', 'image')}),
        (_('Publication'), {
            'fields': (('start_publication', 'end_publication'),
                       'creation_date', 'sites'),
            'classes': ('collapse', 'collapse-closed')}),
        (_('Templates'), {
            'fields': ('content_template', 'detail_template'),
            'classes': ('collapse', 'collapse-closed')}),
        (None, {'fields': ('featured', 'comment_enabled', 'excerpt', 'authors',
                           'related', 'categories', 'tags', 'slug')}))


class ZinniaCategoryAdmin(CategoryAdmin):
    """ Override the CategoryAdmin interface, specifying our own form. """
    form = ZinniaCategoryAdminForm


admin.site.unregister(Entry)
admin.site.register(Entry, ZinniaEntryAdmin)
admin.site.unregister(Category)
admin.site.register(Category, ZinniaCategoryAdmin)

# Remove the third-party items we don't want to see in the admin interface
from django_comments.models import Comment
admin.site.unregister(Comment)


class RedactorFlatPageAdmin(FlatPageAdmin):
    """ Override for the FlatPage admin interface - uses a Redactor widget"""

    form = FlatPageForm
    fieldsets = [
        ('None', {'fields': ['url', 'title', 'sites']}),
        ('Advanced options', {
            'classes': ('collapse',),
            'fields': ('enable_comments', 'registration_required', 'template_name')
        }),
        ('Content', {
            'classes': ('full-width',),
            'fields': ['content']}),
    ]


class ClubInfoAdmin(admin.ModelAdmin):
    """ Admin interface definition for the ClubInfo model. """
    list_display = ('key', 'value')


class ContactSubmissionAdmin(admin.ModelAdmin):
    """ Admin interface definition for the ContactSubmission model. """
    list_display = ('full_name', 'email', 'submitted')


class JuniorsContactSubmissionAdmin(admin.ModelAdmin):
    """ Admin interface definition for the JuniorsContactSubmission model. """
    ordering = ('child_age', 'child_gender', 'child_name')
    list_filter = ('child_age', 'child_gender')
    search_fields = ('full_name', 'child_name', 'email')
    list_display = ('full_name', 'email', 'child_name', 'child_age', 'child_gender', 'submitted')

###############################################################################
# USERS


class CshcUserAdmin(UserAdmin):
    """ Admin interface for the custom auth user model, CshcUser. """

    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('first_name', 'last_name', 'email', 'is_staff')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser',
                                    'groups', 'user_permissions')}),
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
admin.site.unregister(FlatPage)
admin.site.register(FlatPage, RedactorFlatPageAdmin)
admin.site.register(ClubInfo, ClubInfoAdmin)
admin.site.register(ContactSubmission, ContactSubmissionAdmin)
admin.site.register(JuniorsContactSubmission, JuniorsContactSubmissionAdmin)
admin.site.register(CshcUser, CshcUserAdmin)
