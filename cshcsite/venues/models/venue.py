import logging
from django.db import models
from django.template.defaultfilters import slugify

log = logging.getLogger(__name__)


class VenueManager(models.Manager):
    """Model manager for the Venue model"""

    def home_venues(self):
        """Returns only home venues"""
        return super(VenueManager, self).get_query_set().filter(is_home=True)


class Venue(models.Model):
    """Represents a match venue"""

    name = models.CharField("Venue Name", max_length=255, default=None, unique=True)
    """The name of the venue"""

    short_name = models.CharField("Short name", max_length=30, default=None)
    """A shortened/abbreviated venue name"""

    slug = models.SlugField("Slug")
    """Auto-generated slug for the venue"""

    url = models.URLField("Website", blank=True)
    """An optional external web link for the venue"""

    is_home = models.BooleanField("Home ground", default=False)
    """True if this is a home venue"""

    phone = models.CharField("Contact phone number", max_length=20, blank=True)
    """Contact phone number for the venue"""

    addr1 = models.CharField("Address 1", max_length=255, blank=True)
    """First line of the venue address"""

    addr2 = models.CharField("Address 2", max_length=255, blank=True)
    """Second line of the venue address"""

    addr3 = models.CharField("Address 3", max_length=255, blank=True)
    """Third line of the venue address"""

    addr_city = models.CharField("City", max_length=255, blank=True)
    """City line of the venue address"""

    addr_postcode = models.CharField("Post Code", max_length=10, blank=True)
    """Post-code line of the venue address"""

    notes = models.TextField("Notes", blank=True)
    """Any additional notes about this venue. This can be HTML"""

    distance = models.PositiveSmallIntegerField("Distance to this venue", null=True)
    """Distance to this venue from the centre of Cambridge"""

    
    objects = VenueManager()

    class Meta:
        app_label = 'venues'
        ordering = ['name']

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto-populate the slug field
        self.slug = slugify(self.short_name)
        super(Venue, self).save(*args, **kwargs) 

    @models.permalink
    def get_absolute_url(self):
        return ('venue_detail', [self.slug])

    def full_address(self):
        """ Returns the full address with (not None) address items separated by commas."""
        return ", ".join(filter(None, (self.addr1, self.addr2, self.addr3, self.addr_city, self.addr_postcode)))

    def simple_name(self):
        """Returns 'Away' if this is not a home venue. Otherwise returns the short_name attribute value."""
        if(self.is_home):
            return self.short_name
        return "Away"