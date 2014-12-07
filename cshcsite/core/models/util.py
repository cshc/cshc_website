""" Common model utility methods.
"""

import uuid
from django.conf import settings
from model_utils import Choices


def make_unique_filename(filename):
    """ Produces a unique filename, combining the given filename
        and a uuid.
    """
    ext = filename.split('.')[-1]
    return "%s.%s" % (uuid.uuid4(), ext)


def is_none_or_empty(string):
    """ Given a string, returns True if the string is equal to None and is not empty"""
    return string is None or string.strip() == ""


def not_none_or_empty(string):
    """ Given a string, returns True if the string is not equal to None and is not empty"""
    return not is_none_or_empty(string)

# Enumeration of choices for a team's gender. Used in multiple apps.
TeamGender = Choices('Mens', 'Ladies', 'Mixed')

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
    """ Given a team ordinal, returns the actual ordinal part (stripping off the leading 'T')"""
    return team_ordinal.lstrip('T')

def splitify(text):
    """ Ensures a SPLIT_MARKER is inserted after the first paragraph of text.
        Returns the text with the SPLIT_MARKER.

        Ref: https://django-model-utils.readthedocs.org/en/latest/fields.html#splitfield
    """
    if text:
        if not settings.SPLIT_MARKER in text:
            if '</p><p>' in text:
                text = text.replace('</p><p>', '</p>\r\n{}\r\n<p>'.format(settings.SPLIT_MARKER), 1)
    return text
