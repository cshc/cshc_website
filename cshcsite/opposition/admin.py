""" Configuration of Opposition models for the Django admin interface.
"""

from django.contrib import admin
from django.forms import ModelForm
from opposition.models import Club, Team

class TeamInlineForm(ModelForm):
    """ Inline form for a Team model"""

    class Meta:
        """ Meta-info for the form."""
        model = Team


class TeamInline(admin.TabularInline):
    """ Inline admin interface for a Team model.

        This allows teams to be added inline when editing a club.
    """

    model = Team
    form = TeamInlineForm
    extra = 0
    can_delete = False
    exclude = ('slug',)


class ClubAdmin(admin.ModelAdmin):
    """ Admin interface definition for the Club model"""

    readonly_fields = ('slug',)
    inlines = (TeamInline,)
    list_display = ('name', 'website', 'kit_clash_men', 'kit_clash_ladies',
                    'kit_clash_mixed', 'default_venue')
    search_fields = ('name',)


class TeamAdmin(admin.ModelAdmin):
    """ Admin interface definition for the Team model"""

    readonly_fields = ('slug',)
    search_fields = ('name',)
    list_filter = ('club', 'gender')
    list_display = ('name', 'short_name', 'club', 'gender')


# Register all opposition models with the admin interface
admin.site.register(Club, ClubAdmin)
admin.site.register(Team, TeamAdmin)
