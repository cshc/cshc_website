from django.contrib import admin
from .models import ClubTeam, TeamCaptaincy, ClubTeamSeasonParticipation


class TeamCaptaincyInline(admin.TabularInline):
    """Inline for team captaincy - allows quick editing of captains in a team"""

    model = TeamCaptaincy
    extra = 0
    verbose_name_plural = 'Captains'
    ordering = ('-start',)


class ClubTeamAdmin(admin.ModelAdmin):
    """Admin interface for a ClubTeam"""
    readonly_fields = ('slug',)
    inlines = (TeamCaptaincyInline, )
    list_display = ('short_name', 'long_name', 'slug', 'southerners', 'rivals', 'fill_blanks', 'personal_stats')


class ClubTeamSeasonParticipationAdmin(admin.ModelAdmin):
    search_fields = ('team__name', 'division__name')
    list_filter = ('team', 'season')
    list_display = ('__unicode__', 'team', 'season', 'division', 'division_tables_url', 'final_pos', 'division_result')

# Register all teams models with the admin interface
admin.site.register(ClubTeam, ClubTeamAdmin)
admin.site.register(TeamCaptaincy)
admin.site.register(ClubTeamSeasonParticipation, ClubTeamSeasonParticipationAdmin)
