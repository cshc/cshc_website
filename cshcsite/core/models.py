import logging
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils.http import urlquote
from django.core.urlresolvers import reverse
from model_utils import Choices

log = logging.getLogger(__name__)


def is_none_or_empty(s):
    """Given a string, returns True if the string is equal to None and is not empty"""
    return s is None or s.strip() == ""


def not_none_or_empty(s):
    """Given a string, returns True if the string is not equal to None and is not empty"""
    return not is_none_or_empty(s)


def first_or_none(q):
    """ Given a QuerySet or a list, returns the first item, or None if the QuerySet/list is empty."""
    try:
        return q[0]
    except IndexError:
        return None

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
    """Given a team ordinal, returns the actual ordinal part (stripping off the leading 'T')"""
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
        return unicode("{}: {}".format(self.key, self.value))


class ContactSubmission(models.Model):
    """This model is used to store submitted contact form details"""

    # Required attributes:
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField("email address")
    mailing_list = models.BooleanField("Add to mailing list", default=False, help_text="If you select 'yes', we'll add you to our club mailing list. Don't worry - its easy to unsubscribe too!")

    # Optional attributes:
    phone = models.CharField("Phone number", max_length=30, blank=True)
    message = models.TextField("Message", help_text="Message (comments/questions etc)")
    our_notes = models.TextField(blank=True, help_text="Any notes from the club about this enquiry")

    # Automatically created attributes
    submitted = models.DateTimeField("Date submitted", auto_now_add=True, editable=False)

    class Meta:
        app_label = 'core'
        ordering = ['submitted']

    def __unicode__(self):
        return unicode("{} ({})".format(self.full_name(), self.submitted))

    def full_name(self):
        """Full name of the person making the enquiry"""
        return "{} {}".format(self.first_name, self.last_name)


class CshcUserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address')
        email = BaseUserManager.normalize_email(email)
        user = self.model(email=email,
                          is_staff=False, is_active=True, is_superuser=False,
                          last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.save(using=self._db)
        return u


    def make_random_password(self, length=10,
                             allowed_chars='abcdefghjkmnpqrstuvwxyz'
                                           'ABCDEFGHJKLMNPQRSTUVWXYZ'
                                           '23456789'):
        """
        Generates a random password with the given length and given
        allowed_chars. Note that the default value of allowed_chars does not
        have "I" or "O" or letters and digits that look similar -- just to
        avoid confusion.
        """
        return get_random_string(length, allowed_chars)


class CshcUser(AbstractBaseUser, PermissionsMixin):

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['first_name', 'last_name']

    email = models.EmailField(verbose_name='email address', unique=True, db_index=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    is_staff = models.BooleanField('staff status', default=False, help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField('active', default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    objects = CshcUserManager()

    class Meta:
        verbose_name = 'user'
        verbose_name_plural = 'users'
        app_label = 'core'
        ordering = ['first_name', 'last_name']

    def __unicode__(self):
        return unicode(self.email)

    def get_full_name(self):
        return "{} {}".format(self.first_name, self.last_name).strip()

    def get_short_name(self):
        return self.first_name.strip()

    def email_user(self, subject, message, from_email=None):
        """
        Sends an email to this User.
        """
        send_mail(subject, message, from_email, [self.email])
