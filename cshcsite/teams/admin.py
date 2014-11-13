from django.contrib import admin
from .models import ClubTeam, TeamCaptaincy, ClubTeamSeasonParticipation
from .forms import ClubTeamSeasonParticipationForm


class TeamCaptaincyInline(admin.TabularInline):
    """Inline for team captaincy - allows quick editing of captains in a team"""

    model = TeamCaptaincy
    extra = 0
    verbose_name_plural = 'Captains'
    ordering = ('-start',)


class TeamCaptaincyAdmin(admin.ModelAdmin):
    """ Admin interface for a TeamCaptaincy """
    list_display = ('member', 'team', 'season', 'start', 'is_vice')
    search_fields = ('member', 'team', 'season')
    list_filter = ('season', 'is_vice', 'team')

class ClubTeamAdmin(admin.ModelAdmin):
    """Admin interface for a ClubTeam"""
    readonly_fields = ('slug',)
    inlines = (TeamCaptaincyInline, )
    list_display = ('short_name', 'long_name', 'slug', 'southerners', 'rivals', 'fill_blanks', 'personal_stats')


class ClubTeamSeasonParticipationAdmin(admin.ModelAdmin):
    form = ClubTeamSeasonParticipationForm
    search_fields = ('team__name', 'division__name')
    list_filter = ('team', 'season')
    list_display = ('__unicode__', 'team', 'season', 'division', 'division_tables_url', 'final_pos', 'division_result')
    fieldsets = [
        ('Basics', {
            'fields': ['team', 'season', 'division', 'blurb', 'team_photo',
            'team_photo_caption']
        }),
        ('Links', {
            'fields': ['division_tables_url', 'division_fixtures_url']
        }),
        ('Cup', {
            'fields': ['cup', 'cup_result']
        }),
        ('Result', {
            'fields': ['final_pos', 'division_result']
        }),
    ]

# Register all teams models with the admin interface
admin.site.register(ClubTeam, ClubTeamAdmin)
admin.site.register(TeamCaptaincy, TeamCaptaincyAdmin)
admin.site.register(ClubTeamSeasonParticipation, ClubTeamSeasonParticipationAdmin)
