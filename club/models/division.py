from django.db import models
from choices import TEAM_GENDER
from league import League

class Division(models.Model):
    name = models.CharField("Division Name", max_length=255)
    league = models.ForeignKey(League, related_name="Divisions", help_text="The league that is responsible for this division")
    tables_url = models.URLField("League table website", null=True, blank=True)
    fixtures_url = models.URLField("Fixtures website", null=True, blank=True)
    gender = models.CharField("Division gender (mens/ladies)", max_length=2, choices=TEAM_GENDER)

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
