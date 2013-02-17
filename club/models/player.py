from django.db import models
from choices import PlayerGender, PlayerPosition
from match import Match

class Player(models.Model):
    first_name = models.CharField("First name", max_length=255)
    surname = models.CharField("Surname", max_length=255)
    gender = models.CharField("Gender", max_length=1, choices=PlayerGender.CHOICES)
    pref_position = models.CharField("Preferred position", max_length=3, choices=PlayerPosition.CHOICES)
   
    appearances = models.ManyToManyField(Match, through="Appearance")

    class Meta:
        app_label = 'club'
 
    def __unicode__(self):
        return "{} {}".format(self.first_name, self.surname)


