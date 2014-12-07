""" Custom auth user model.

    Uses an email address as a username.
"""

from django.utils import timezone
from django.utils.crypto import get_random_string
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.mail import send_mail


class CshcUserManager(BaseUserManager):
    """ Management of the custom CshcUser model. """

    def create_user(self, email, password=None, **extra_fields):
        """ Creates and saves a User with the given email and password. """
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
        """ Creates a superuser. """
        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


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
    """ Custom auth user model.

        Uses email address instead of the username.
    """

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['first_name', 'last_name']

    email = models.EmailField(verbose_name='email address', unique=True, db_index=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    is_staff = models.BooleanField('staff status', default=False,
                                   help_text='Designates whether the user can log into this admin site.')
    is_active = models.BooleanField('active', default=True,
                                    help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.')
    date_joined = models.DateTimeField('date joined', default=timezone.now)

    objects = CshcUserManager()

    class Meta:
        """ Meta-info for the CshcUser model. """
        verbose_name = 'user'
        verbose_name_plural = 'users'
        app_label = 'core'
        ordering = ['first_name', 'last_name']

    def __unicode__(self):
        return unicode("{} {} ({})".format(self.first_name, self.last_name, self.email))

    def get_full_name(self):
        return u"{} {}".format(self.first_name, self.last_name).strip()

    def get_short_name(self):
        return unicode(self.first_name.strip())

    def email_user(self, subject, message, from_email=None):
        """ Sends an email to this User. """
        send_mail(subject, message, from_email, [self.email])
