# During a match, people can use the website to add 'live commentary'
# on the proceedings, including goals scored/conceeded, regular text
# updates and photos. The MatchComment model captures a single (timestamped)
# comment. Comments are always associated with a particular match and
# an 'author' (only logged in users can post comments).

# To avoid multiple people recording that a goal was scored,
# one person and only one person can be the official match commentator.
# Initially when the match page is viewed, if you are logged in you
# will have an option to make yourself the match commentator. After
# this point, no-one else will be able to make themselves match commentator.
# You will then have additional priviledges and options (e.g. to record
# goals scored/conceeded and to delete comments). At any time that person
# can relinquish his/her role as commentator - at which point someone
# else could take over.

from django.db import models
from django.core.exceptions import ValidationError
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManager
from model_utils import Choices
from core.models import is_none_or_empty, CshcUser
from matches.models import Match



class MatchCommentQuerySet(QuerySet):
    """ Queries that relate to Matches"""

    def by_author(self, author):
        return self.filter(author=author)

    def by_match(self, match_id):
        return self.filter(match__id=match_id)

    def since(self, match_id, last_update):
        return self.filter(match__id=match_id, timestamp__gt=last_update)


class MatchComment(models.Model):

    COMMENT_TYPE = Choices((0, 'Scored', 'Goal scored'),
                           (1, 'Conceeded', 'Goal conceeded'),
                           (2, 'Photo', 'Photo'),
                           (3, 'Update', 'Update'))

    STATE = Choices('Pending', 'Approved', 'Rejected', 'Deleted')

    author = models.ForeignKey(CshcUser, null=True, blank=True, on_delete=models.SET_NULL)
    match = models.ForeignKey(Match)

    comment_type = models.IntegerField("Comment Type", choices=COMMENT_TYPE, default=COMMENT_TYPE.Update)

    comment = models.TextField("Comment", blank=True)

    # An optional photo
    photo = models.ImageField("Photo", upload_to='uploads/match_photos', null=True, blank=True)

    state = models.CharField("State", max_length=10, choices=STATE, default=STATE.Approved)

    # Automatically created attribute
    timestamp = models.DateTimeField("Timestamp", auto_now_add=True, editable=False)
    last_modified = models.DateTimeField("Last modified", auto_now=True, editable=False)

    objects = PassThroughManager.for_queryset_class(MatchCommentQuerySet)()

    class Meta:
        app_label = 'matches'
        ordering = ['-timestamp']

    def clean(self):
        if self.comment_type == MatchComment.COMMENT_TYPE.Update and is_none_or_empty(self.comment):
            raise ValidationError("A comment must be supplied for an 'update' match comment")

        if self.comment_type == MatchComment.COMMENT_TYPE.Photo and self.photo is None:
            raise ValidationError("A photo must be supplied for a 'photo' match comment")

    def __unicode__(self):
        return unicode("{}: {} ({})".format(self.timestamp.strftime('%X %x'), self.get_comment_type_display(), self.author))
