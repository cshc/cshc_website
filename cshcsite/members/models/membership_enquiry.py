import logging
from django.db import models

log = logging.getLogger(__name__)


class MembershipEnquiry(models.Model):
    """This model is used to store membership enquiries"""

    # Required attributes:
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField("email address")
    mailing_list = models.BooleanField("Add to mailing list", default=False, help_text="If you select 'yes', we'll add you to our club mailing list. Don't worry - its easy to unsubscribe too!")

    # Optional attributes:
    phone  = models.CharField(max_length=20, blank=True)
    prev_experience = models.TextField("Previous hockey experience", blank=True, help_text="A brief description of any previous hockey experience")
    comments = models.TextField("Comments/Questions", blank=True, help_text="Any other comments or questions")
    our_notes = models.TextField(blank=True, help_text="Any notes from the club about this enquiry")
    
    # Automatically created attributes
    submitted = models.DateTimeField("Date submitted", auto_now_add=True, editable=False)

    class Meta:
        app_label = 'members'
        ordering = ['submitted']

    def __unicode__(self):
        return "{} ({})".format(self.full_name, self.submitted)

    @models.permalink
    def get_absolute_url(self):
        return ('membershipenquiry_detail', [self.pk])

    def full_name(self):
        """Full name of the person making the enquiry"""
        return "{} {}".format(self.first_name, self.last_name)