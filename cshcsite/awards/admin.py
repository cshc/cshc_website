from django.contrib import admin
from .models import MatchAward, EndOfSeasonAward, MatchAwardWinner, EndOfSeasonAwardWinner


# Register all awards models with the admin system
admin.site.register(MatchAward)
admin.site.register(EndOfSeasonAward)
admin.site.register(MatchAwardWinner)
admin.site.register(EndOfSeasonAwardWinner)
