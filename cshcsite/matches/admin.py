from django.contrib import admin
from django.forms import ModelForm, widgets
from suit.widgets import NumberInput, AutosizedTextarea
from awards.models import MatchAwardWinner
from .models import Match, Appearance
from .forms import MatchForm


class MatchAwardWinnerInlineForm(ModelForm):
    """Inline form for match award winners"""

    class Meta:
        model = MatchAwardWinner
        widgets = {
            'comment': AutosizedTextarea(
                attrs={'class': 'input-medium', 'rows': 2,
                       'style': 'width:95%'}),
        }


class MatchAwardWinnerInline(admin.TabularInline):
    """Inline for match award winners - allows quick editing of award winners in a match"""

    model = MatchAwardWinner
    form = MatchAwardWinnerInlineForm
    extra = 0
    verbose_name_plural = 'Award winners'


class AppearanceInlineForm(ModelForm):
    """Inline form for appearances"""

    class Meta:
        model = Appearance
        widgets = {
            'goals': NumberInput(attrs={'class': 'input-mini'}),
            'own_goals': NumberInput(attrs={'class': 'input-mini'}),
            'green_card': widgets.NullBooleanSelect(attrs={'class': 'input-small'}),
            'yellow_card': widgets.NullBooleanSelect(attrs={'class': 'input-small'}),
            'red_card': widgets.NullBooleanSelect(attrs={'class': 'input-small'}),
        }


class AppearanceInline(admin.TabularInline):
    """Inline for appearances - allows quick editing of appearances in a match"""
    model = Appearance
    form = AppearanceInlineForm
    extra = 0
    verbose_name_plural = 'Appearances'


class MatchAdmin(admin.ModelAdmin):
    """Model Admin for matches"""

    form = MatchForm
    inlines = (MatchAwardWinnerInline, AppearanceInline)
    radio_fields = {'fixture_type': admin.HORIZONTAL, 'home_away': admin.HORIZONTAL, 'alt_outcome': admin.HORIZONTAL}
    fieldsets = [
        ('Teams', {'fields': ['our_team', 'opp_team']}),
        ('Fixture details', {'fields': ['venue', 'home_away', 'fixture_type', 'date', 'time']}),
        ('Result', {'fields': ['alt_outcome', 'our_score', 'opp_score', 'our_ht_score', 'opp_ht_score', 'opp_own_goals']}),
        ('Advanced', {'fields': ['ignore_for_goal_king', 'ignore_for_southerners', 'override_kit_clash', 'gpg_pro_rata']}),
        ('Pre-match hype', {
            'classes': ('full-width',),
            'fields': ['pre_match_hype']}),

        ('Report details', {'fields': ['report_title', 'report_author']}),

        ('Match report', {
            'classes': ('full-width',),
            'fields': ['report_body']}),
    ]
    list_display = ('date', 'our_team', 'opp_team', 'venue')
    search_fields = ('our_team', 'opp_team', 'venue')
    list_filter = ('our_team', 'opp_team', 'venue', 'fixture_type', 'home_away')


class AppearanceAdmin(admin.ModelAdmin):

    model = Appearance
    search_fields = ('member',)
    list_filter = ('green_card', 'yellow_card', 'red_card')


# Register matches models with the admin system
admin.site.register(Match, MatchAdmin)
admin.site.register(Appearance, AppearanceAdmin)
# NOTE: We do not register the GoalKing model - this is derived from other models
# and should never be edited via the admin interface
