""" The Member model represents a club member - specifically someone who
    participates in matches or holds a committee position.

    Members may be linked to website Users (CshcUser) - this enables the
    user's profile page to display stats and details pertaining to their
    member model. In particular, it lets the user upload a profile picture
    for their member model.
"""

import os
from django.conf import settings
from django.db import models
from django_resized import ResizedImageField
from model_utils import Choices
from core.models import make_unique_filename


def get_file_name(instance, filename):
    """ Returns a unique filename for profile pictures."""
    filename = make_unique_filename(filename)
    return os.path.join('uploads/profile_pics', filename)


class MemberManager(models.Manager):

    def get_query_set(self):
        return super(MemberManager, self).get_query_set().extra(select={"pref_name":"COALESCE(NULLIF(known_as, ''), first_name)"}, order_by=["pref_name", "last_name"])


class Member(models.Model):
    """ Represents a member of Cambridge South Hockey Club. Alternatively this can
        be thought of as a 'Player' model.

        User accounts will be associated with a member instance wherever possible.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True,
                                on_delete=models.SET_NULL)

    # Members first name (required)
    first_name = models.CharField(max_length=100, default=None)

    # The first name by which the member is typically known (optional)
    known_as = models.CharField(max_length=100, default=None, null=True, blank=True)

    # Members surname (required)
    last_name = models.CharField(max_length=100, default=None)

    # Members can be either male or female. That's all. Deal with it!
    GENDER = Choices('Male', 'Female')

    # Each member has a preferred position (or unknown)
    POSITION = Choices((0, 'GK', 'Goalkeeper'),
                       (1, 'GK_Def', 'Goalkeeper/Defender'),
                       (2, 'GK_Mid', 'Goalkeeper/Midfielder'),
                       (3, 'GK_Fwd', 'Goalkeeper/Forward'),
                       (4, 'Def', 'Defender'),
                       (5, 'Def_Mid', 'Defender/Midfielder'),
                       (6, 'Mid', 'Midfielder'),
                       (7, 'Mid_Fwd', 'Midfielder/Forward'),
                       (8, 'Fwd', 'Forward'),
                       (9, 'Other', 'Not known'))

    # An optional profile picture of the member
    profile_pic = ResizedImageField("Profile picture", max_width=400, max_height=400,
                                    upload_to=get_file_name, null=True, blank=True)

    # The member's gender
    gender = models.CharField("Gender", max_length=6, choices=GENDER, default=GENDER.Male)

    # The member's preferred playing position. Defaults to 'not known'.
    pref_position = models.IntegerField("Preferred position", choices=POSITION,
                                        default=POSITION.Other)

    # Indicates whether this member is a current member of the club. Useful for filtering etc.
    is_current = models.BooleanField(default=True)

    # Players shirt number
    shirt_number = models.CharField(max_length=4, blank=True)

    objects = MemberManager()

    class Meta:
        """ Meta-info for the Member model."""
        app_label = 'members'
        ordering = ['first_name', 'last_name']

    def __unicode__(self):
        return unicode(self.full_name())

    @models.permalink
    def get_absolute_url(self):
        """ Returns the url for this member instance."""
        return ('member_detail', [self.pk])

    def pref_first_name(self):
        """ Returns the member's preferred first name (known_as if set; otherwise first_name) """
        return self.known_as if self.known_as else self.first_name

    def full_name(self):
        """ Returns the member's full name."""
        return u"{} {}".format(self.pref_first_name(), self.last_name)

    def first_name_and_initial(self):
        """ Returns the shortened name display for this member."""
        return u"{} {}".format(self.pref_first_name(), self.last_name[0])
