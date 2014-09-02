from .models import MatchComment
from rest_framework import serializers


class MatchCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = MatchComment
        fields = ('id', 'author', 'match', 'comment_type', 'comment', 'photo', 'state', 'timestamp', 'last_modified')
