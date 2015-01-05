from django.contrib import admin
from django.forms import ModelForm
import autocomplete_light
from suit.widgets import AutosizedTextarea
from .models import MatchComment, MatchCommentator

class MatchCommentInlineForm(ModelForm):
    """Inline form for match comments"""

    class Meta:
        model = MatchComment
        widgets = {
            'comment': AutosizedTextarea(
                attrs={'class': 'input-medium', 'rows': 2,
                       'style': 'width:95%'}),
        }


class MatchCommentInline(admin.TabularInline):
    """Inline for match comments"""

    model = MatchComment
    form = MatchCommentInlineForm
    exclude = ('state', 'photo')
    extra = 0


class MatchCommentAdmin(admin.ModelAdmin):

    model = MatchComment
    search_fields = ('author',)
    list_filter = ('author',)
    list_display = ('author', 'match', 'comment', 'comment_type', 'timestamp', 'photo')
    form = autocomplete_light.modelform_factory(MatchComment)



class MatchCommentatorAdmin(admin.ModelAdmin):

    model = MatchCommentator
    search_fields = ('commentator', 'match')
    list_filter = ('commentator',)
    list_display = ('commentator', 'match')
    form = autocomplete_light.modelform_factory(MatchCommentator)


admin.site.register(MatchComment, MatchCommentAdmin)
admin.site.register(MatchCommentator, MatchCommentatorAdmin)