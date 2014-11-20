from .models import MatchComment
from rest_framework import serializers
import autocomplete_light


class MatchCommentSerializer(serializers.ModelSerializer):
    match = serializers.ChoiceField(widget=autocomplete_light.ChoiceWidget('MatchAutocomplete'))
    author = serializers.ChoiceField(widget=autocomplete_light.ChoiceWidget('CshcUserAutocomplete'))

    class Meta:
        model = MatchComment
        fields = ('id', 'author', 'match', 'comment_type', 'comment', 'photo', 'state', 'timestamp', 'last_modified')
