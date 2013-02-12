from django.db import models
from choices import TeamGender
from league import League
from django.db import IntegrityError

class Division(models.Model):
    name = models.CharField("Division Name", max_length=255, default=None)
    league = models.ForeignKey(League, related_name="Divisions", help_text="The league that is responsible for this division")
    tables_url = models.URLField("League table website", null=True, blank=True, default=None)
    fixtures_url = models.URLField("Fixtures website", null=True, blank=True, default=None)
    gender = models.CharField("Division gender (mens/ladies)", max_length=2, choices=TeamGender.CHOICES, default=None)

    # The division structure is represented by specifying the division into which teams get promoted
    # or relegated from this division. 
    # A null value indicates that it is not possible to get promoted or relegated from this division.
    # Note we set related_name to to "+" so Django won't create a backwards relationship
    promotion_div = models.ForeignKey('self', related_name="+", null=True, verbose_name="Next division up", help_text="The division (if any) into which promoted teams will move", on_delete=models.SET_NULL)
    relegation_div = models.ForeignKey('self', related_name="+", null=True, verbose_name="Next division down", help_text="The division (if any) into which relegated teams will move", on_delete=models.SET_NULL)

    class Meta:
        app_label = 'club'
        # A division's name must be unique within a league. 
        # However two different leagues can have divisions with the same name
        unique_together = ('name', 'league',)   

    def __unicode__(self):
        return "{} {}".format(self.league.name, self.name)

    def save(self, *args, **kwargs):
        # Note that this does not check for larger 'circular promotion/relegation references'
        if (self.promotion_div != None and 
            self.relegation_div != None and 
            self.promotion_div == self.relegation_div):
            raise IntegrityError("Promotion and relegation divisions cannot be the same")
        
        super(Division, self).save(*args, **kwargs) 
