from django.contrib import admin
from django.forms import ModelForm, widgets
from .models import League, Division, Season, Cup


class CupInline(admin.TabularInline):
    """Inline for cups - allows quick editing of cups in a league"""
    
    model = Cup
    extra = 0


class DivisionInlineForm(ModelForm):
    """Inline form for divisions"""

    class Meta:
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
    model = Division
    list_display = ('league', 'name', 'gender')
    list_filter = ('league', 'gender')
    search_fields = ('league', 'name')


class LeagueAdmin(admin.ModelAdmin):
    """Admin interface for the League model"""
    # Allow quick editing of divisions within a league
    model = League
    inlines = (DivisionInline, CupInline)
    list_display = ('name', 'url')
    search_fields = ('name',)


class SeasonAdmin(admin.ModelAdmin):
    """Admin interface for the Season model"""
    model = Season
    readonly_fields = ('slug',)


# Register all competitions models with the admin system
admin.site.register(League, LeagueAdmin)
admin.site.register(Division, DivisionAdmin)
admin.site.register(Season, SeasonAdmin)
admin.site.register(Cup)
