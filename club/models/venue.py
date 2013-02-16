from django.db import models

class Venue(models.Model):
    name = models.CharField("Venue Name", max_length=255)
    short_name = models.CharField("Short name", max_length=30)
    url = models.URLField("Website", null=True, blank=True, default=None)
    phone = models.CharField("Contact phone number", max_length=20, null=True, blank=True, default=None)
    addr1 = models.CharField("Address 1", max_length=255, null=True, blank=True, default=None)
    addr2 = models.CharField("Address 2", max_length=255, null=True, blank=True, default=None)
    addr3 = models.CharField("Address 3", max_length=255, null=True, blank=True, default=None)
    addr_city = models.CharField("City", max_length=255, null=True, blank=True, default=None)
    addr_postcode = models.CharField("Post Code", max_length=10, null=True, blank=True, default=None)
    notes = models.TextField("Notes", null=True, blank=True, default=None)

    class Meta:
        app_label = 'club'

    def __unicode__(self):
        return self.name