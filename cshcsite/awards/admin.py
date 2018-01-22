""" Configuration of Award models for the Django admin interface.
"""

from django.contrib import admin
from awards.models import MatchAward, EndOfSeasonAward, MatchAwardWinner, EndOfSeasonAwardWinner


class MatchAwardWinnerAdmin(admin.ModelAdmin):
    """ Admin interface definition for the MatchAwardWinner model."""
    model = MatchAwardWinner
    search_fields = ('member__first_name', 'member__known_as', 'member__last_name')
    list_display = ('__unicode__', 'member', 'awardee', 'award', 'match')
    list_filter = ('award',)


class EndOfSeasonAwardWinnerAdmin(admin.ModelAdmin):
    """ Admin interface definition for the EndOfSeasonAwardWinner model."""
    model = EndOfSeasonAwardWinner
    search_fields = ('member__first_name', 'member__known_as', 'member__last_name')
    list_display = ('__unicode__', 'member', 'awardee', 'award', 'season')
    list_filter = ('award', 'season')


# Register all awards models with the admin system
admin.site.register(MatchAward)
admin.site.register(EndOfSeasonAward)
admin.site.register(MatchAwardWinner, MatchAwardWinnerAdmin)
admin.site.register(EndOfSeasonAwardWinner, EndOfSeasonAwardWinnerAdmin)
