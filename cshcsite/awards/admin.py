from django.contrib import admin
from .models import MatchAward, EndOfSeasonAward, MatchAwardWinner, EndOfSeasonAwardWinner


class MatchAwardWinnerAdmin(admin.ModelAdmin):
    model = MatchAwardWinner
    search_fields = ('member__firstname', 'member__lastname')
    list_display = ('__unicode__', 'member', 'awardee', 'award', 'match')
    list_filter = ('award',)


class EndOfSeasonAwardWinnerAdmin(admin.ModelAdmin):
    model = EndOfSeasonAwardWinner
    search_fields = ('member__firstname', 'member__lastname')
    list_display = ('__unicode__', 'member', 'awardee', 'award', 'season')
    list_filter = ('award', 'season')


# Register all awards models with the admin system
admin.site.register(MatchAward)
admin.site.register(EndOfSeasonAward)
admin.site.register(MatchAwardWinner, MatchAwardWinnerAdmin)
admin.site.register(EndOfSeasonAwardWinner, EndOfSeasonAwardWinnerAdmin)
