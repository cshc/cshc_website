""" Configuration of Competition models for the Django admin interface.
"""

from django.contrib import admin
from django.forms import ModelForm, widgets
from competitions.models import League, Division, Season, Cup


class CupInline(admin.TabularInline):
    """Inline for cups - allows quick editing of cups in a league"""

    model = Cup
    extra = 0


class DivisionInlineForm(ModelForm):
    """Inline form for divisions"""

    class Meta:
        """ Meta-info for the form."""
        model = Division
        widgets = {
            'gender': widgets.Select(attrs={'class': 'input-small'}),
        }


class DivisionInline(admin.TabularInline):
    """Inline for divisions - allows quick editing of divisions in a league"""

    model = Division
    form = DivisionInlineForm
    extra = 0


class DivisionAdmin(admin.ModelAdmin):
    """ Admin interface definition for the Division model."""
    model = Division
    list_display = ('__unicode__', 'league', 'name', 'gender')
    list_filter = ('league', 'gender')
    search_fields = ('league__name', 'name')


class LeagueAdmin(admin.ModelAdmin):
    """Admin interface definition for the League model"""
    model = League
    # Allow quick editing of divisions within a league
    inlines = (DivisionInline, CupInline)
    list_display = ('name', 'url')
    search_fields = ('name',)


class SeasonAdmin(admin.ModelAdmin):
    """Admin interface definition for the Season model"""
    model = Season
    list_display = ('__unicode__', 'start', 'end')
    readonly_fields = ('slug',)


# Register all competitions models with the admin system
admin.site.register(League, LeagueAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Cup)
