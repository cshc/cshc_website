""" Storage of 'Contact Us' form submissions.
"""

from django.db import models


class ContactSubmission(models.Model):
    """This model is used to store submitted contact form details"""

    # Required attributes:
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField("email address")
    mailing_list = models.BooleanField("Add to mailing list", default=False,
                                       help_text="If you select 'yes', we'll add you to our club mailing list. Don't worry - its easy to unsubscribe too!")

    # Optional attributes:
    phone = models.CharField("Phone number", max_length=30, blank=True)
    message = models.TextField("Message", help_text="Message (comments/questions etc)")
    our_notes = models.TextField(blank=True, help_text="Any notes from the club about this enquiry")

    # Automatically created attributes
    submitted = models.DateTimeField("Date submitted", auto_now_add=True, editable=False)

    class Meta:
        """ Meta-info for the ContactSubmission model. """
        app_label = 'core'
        ordering = ['submitted']

    def __unicode__(self):
        return unicode("{} ({})".format(self.full_name(), self.submitted))

    def full_name(self):
        """ Full name of the person making the enquiry"""
        return u"{} {}".format(self.first_name, self.last_name)

