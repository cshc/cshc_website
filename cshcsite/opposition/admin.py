from django.contrib import admin
from django.forms import ModelForm
from .models import Club, Team

class TeamInlineForm(ModelForm):
    """Inline form for a Team model"""

    class Meta:
        model = Team
        

class TeamInline(admin.TabularInline):
    """Inline admin interface for a Team model"""

    model = Team
    form = TeamInlineForm
    extra = 0
    can_delete = False
    exclude = ('slug',)


class ClubAdmin(admin.ModelAdmin):
    """Club admin interface"""

    readonly_fields = ('slug',)
    inlines = (TeamInline,)
    list_display = ('name', 'website', 'kit_clash_men', 'kit_clash_ladies', 'kit_clash_mixed', 'default_venue')
    search_fields = ('name',)


class TeamAdmin(admin.ModelAdmin):
    """Team admin interface"""

    readonly_fields = ('slug',)
    search_fields = ('name',)
    list_filter = ('club', 'gender')
    list_display = ('club', 'name', 'gender')

# Register all opposition models with the admin interface
admin.site.register(Club, ClubAdmin)
admin.site.register(Team, TeamAdmin)
