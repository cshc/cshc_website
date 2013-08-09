import logging
from django.conf import settings
from django.db import models
from model_utils import Choices

log = logging.getLogger(__name__)


class Member(models.Model):
    """
    Represents a member of Cambridge South Hockey Club. Alternatively this can
    be thought of as a 'Player' model.

    User accounts will be associated with a member instance wherever possible.
    """

    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)

    # Members first name (required)
    first_name = models.CharField(max_length=100, default=None)

    # Members surname (required)
    last_name = models.CharField(max_length=100, default=None)

    # Members can be either male or female
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
    profile_pic = models.ImageField(upload_to='uploads/profile_pics', null=True, blank=True)

    # The member's gender
    gender = models.CharField("Gender", max_length=6, choices=GENDER, default=GENDER.Male)

    # The member's preferred playing position. Defaults to 'not known'.
    pref_position = models.IntegerField("Preferred position", choices=POSITION, default=POSITION.Other)

    # Indicates whether this member is a current member of the club. Useful for filtering etc.
    is_current = models.BooleanField(default=True)

    class Meta:
        app_label = 'members'
        ordering = ['first_name', 'last_name']

    def __unicode__(self):
        return self.full_name()

    @models.permalink
    def get_absolute_url(self):
        return ('member_detail', [self.pk])

    def full_name(self):
        """
        Returns the member's full name.
        """
        return "{} {}".format(self.first_name, self.last_name)


