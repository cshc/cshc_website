""" Storage of 'Contact Us' form submissions.
"""

from django.db import models
from model_utils import Choices


class JuniorsContactSubmission(models.Model):
    """This model is used to store submitted juniors contact form details"""

    GENDER = Choices(('Male', 'Male'), ('Female', 'Female'))
    AGE = Choices(
        ('ALT6', '< 6'),
        ('A6', '6'),
        ('A7', '7'),
        ('A8', '8'),
        ('A9', '9'),
        ('A10', '10'),
        ('A11', '11'),
        ('A12', '12'),
        ('AGT12', '> 12'))

    # Required attributes:
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField("email address")
    mailing_list = models.BooleanField("Add to mailing list", default=False,
                                       help_text="If you select 'yes', we'll add you to our club mailing list. Don't worry - its easy to unsubscribe too!")

    child_name = models.CharField(max_length=255)
    child_age = models.CharField(max_length=10, choices=AGE, default=AGE.ALT6)
    child_gender = models.CharField(max_length=10, choices=GENDER, default=GENDER.Male)

    # Optional attributes:
    phone = models.CharField("Phone number", max_length=30, blank=True)
    message = models.TextField("Message", help_text="Message (comments/questions etc)", blank=True)
    our_notes = models.TextField(blank=True, help_text="Any notes from the club about this enquiry")

    # Automatically created attributes
    submitted = models.DateTimeField("Date submitted", auto_now_add=True, editable=False)

    class Meta:
        """ Meta-info for the JuniorsContactSubmission model. """
        app_label = 'core'
        ordering = ['submitted']

    def __unicode__(self):
        return unicode("{} ({})".format(self.full_name(), self.submitted))

    def full_name(self):
        """ Full name of the person making the enquiry"""
        return u"{} {}".format(self.first_name, self.last_name)

