from django.db import models
from choices import MemberGender, MemberPosition
from match import Match
from django.contrib.auth.models import User

class Member(models.Model):
    user = models.ForeignKey(User)
    profile_pic = models.ImageField(upload_to='/pics')
    gender = models.CharField("Gender", max_length=1, choices=MemberGender.CHOICES, default=MemberGender.MALE)
    pref_position = models.CharField("Preferred position", max_length=3, choices=MemberPosition.CHOICES, default=MemberPosition.NOT_KNOWN)
   
    appearances = models.ManyToManyField(Match, through="Appearance")

    class Meta:
        app_label = 'club'
        User._meta.ordering = ['first_name', 'last_name']
 
    def __unicode__(self):
        return "{} {}".format(self.first_name, self.surname)


