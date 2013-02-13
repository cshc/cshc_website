from django.db import models
from django.contrib.auth.models import User
from team import Team


class Player(models.Model):
    user = models.ForeignKey(User, editable=False)
    team = models.ForeignKey(Team)
    position = models.CharField(max_length = 20)

    class Meta:
        app_label = 'club'

    def __unicode__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

