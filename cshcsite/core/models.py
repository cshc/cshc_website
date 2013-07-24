import logging
from django.db import models
from model_utils import Choices

log = logging.getLogger(__name__)


def not_none_or_empty(s):
    """Given a string, returns True if the string is not equal to None and is not empty"""
    return s is not None and s.strip() != ""


def first_or_none(q):
    """ Given a QuerySet or a list, returns the first item, or None if the QuerySet/list is empty."""
    try:
        return q[0]
    except IndexError:
        return None

# Enumeration of choices for a team's gender. Used in multiple apps.
TeamGender = Choices('mens', 'ladies', 'mixed')

# Enumeration of choices for a team's ordinal. Used in multiple apps.
TeamOrdinal = Choices(
        ('T1', '1sts'),
        ('T2', '2nds'),
        ('T3', '3rds'),
        ('T4', '4ths'),
        ('T5', '5ths'),
        ('T6', '6ths'),
        ('T7', '7ths'),
        ('T8', '8ths'),
        ('T9', '9ths'),
        ('T10', '10ths'),
        ('T11', '11ths'),
        ('T12', '12ths'),
        ('TVets', 'Vets'),
        ('TIndoor', 'Indoor'),
        ('TOther', 'Other'))


def ordinal_from_TeamOrdinal(team_ordinal):
    """Given a team ordinal, returns the actual ordinal part (stripping off the leading 'T')"""
    return team_ordinal.lstrip('T')


class ClubInfo(models.Model):
    """This model is used as a look-up table for club information where the actual
    value may change over time and needs to be easily editable through the admin backend
    without modification to the templates or Python code that reference it.
    """

    key = models.CharField(max_length=20, unique=True)
    """The look-up key. The value of this field is what is referenced directly in
    template and Python code."""

    value = models.CharField(max_length=100)
    """The lookup value. This is the actual value that is required by the templates
    or Python code."""

    class Meta:
        verbose_name = 'Club Information'
        verbose_name_plural = 'Club Information'
        ordering = ['key']

    def __unicode__(self):
        return "{}: {}".format(self.key, self.value)


class ContactSubmission(models.Model):
    """This model is used to store submitted contact form details"""

    # Required attributes:
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField("email address")
    mailing_list = models.BooleanField("Add to mailing list", default=False, help_text="If you select 'yes', we'll add you to our club mailing list. Don't worry - its easy to unsubscribe too!")

    # Optional attributes:
    phone = models.CharField("Phone number", max_length=30, blank=True)
    message = models.TextField("Message", blank=True, help_text="Message (comments/questions etc)")
    our_notes = models.TextField(blank=True, help_text="Any notes from the club about this enquiry")

    # Automatically created attributes
    submitted = models.DateTimeField("Date submitted", auto_now_add=True, editable=False)

    class Meta:
        app_label = 'core'
        ordering = ['submitted']

    def __unicode__(self):
        return "{} ({})".format(self.full_name(), self.submitted)

    def full_name(self):
        """Full name of the person making the enquiry"""
        return "{} {}".format(self.first_name, self.last_name)
