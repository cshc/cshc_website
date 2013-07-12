import logging
from django.db import models
from types import StringType
from model_utils import Choices

log = logging.getLogger(__name__)


def not_none_or_empty(s):
    """Given a string, returns True if the string is not equal to None and is not empty"""
    return s != None and s.strip() != ""


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