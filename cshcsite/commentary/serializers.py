import autocomplete_light
from rest_framework import serializers
from core.models import CshcUser
from matches.models import Match
from .models import MatchComment, MatchCommentator


class MatchCommentSerializer(serializers.Serializer):

    id = serializers.IntegerField(required=False)
    match = serializers.IntegerField(source='match_id')
    author = serializers.IntegerField(source='author_id')
    author_name = serializers.CharField(source='author.get_full_name', required=False)
    comment = serializers.CharField()
    comment_type = serializers.ChoiceField(choices=MatchComment.COMMENT_TYPE)
    state = serializers.ChoiceField(choices=MatchComment.STATE, required=False)
    photo = serializers.ImageField(required=False)
    timestamp = serializers.DateTimeField(required=False)
    last_modified = serializers.DateTimeField(required=False)

    def restore_object(self, attrs, instance=None):
        """
        Given a dictionary of deserialized field values, either update
        an existing model instance, or create a new model instance.
        """
        if instance is not None:
            instance.comment = attrs.get('comment', instance.comment)
            instance.comment_type = attrs.get('comment_type', instance.comment_type)
            instance.state = attrs.get('state', instance.state)
            #instance.photo = attrs.get('photo', instance.photo)
            return instance
        if 'author.get_full_name' in attrs:
            attrs.pop('author.get_full_name')
        #attrs['match'] = Match.objects.get(id=attrs.pop('match.id'))
        #attrs['author'] = CshcUser.objects.get(id=attrs.pop('author.id'))
        return MatchComment(**attrs)


class MatchCommentatorSerializer(serializers.Serializer):

    id = serializers.IntegerField(required=False)
    match = serializers.IntegerField(source='match_id')
    commentator = serializers.IntegerField(source='commentator_id')
    commentator_name = serializers.CharField(source='commentator.get_full_name', required=False)

    def restore_object(self, attrs, instance=None):
        if instance is not None:
            instance.match_id = attrs.get('match_id', instance.match)
            instance.commentator_id = attrs.get('commentator_id', instance.commentator)
            return instance
        if 'commentator.get_full_name' in attrs:
            attrs.pop('commentator.get_full_name')
        return MatchCommentator(**attrs)