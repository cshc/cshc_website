from django.db import models

class Club(models.Model):
    name = models.CharField("Club Name", max_length=255, unique=True, default=None)
    website = models.URLField("Club Website", null=True, blank=True, default=None)
    kit_clash_men = models.BooleanField("Kit-clash (men)", default=False, help_text="Does this club's mens kit clash with our mens kit?")
    kit_clash_ladies = models.BooleanField("Kit-clash (ladies)", default=False, help_text="Does this club's ladies kit clash with our ladies kit?")
    kit_clash_mixed = models.BooleanField("Kit-clash (mixed)", default=False, help_text="Does this club's mixed team kit clash with our mixed team kit?")

    class Meta:
        app_label = 'club'
        ordering = ['name']

    def __unicode__(self):
        return self.name
        
    @staticmethod
    def our_club():
        return Club.objects.get(name='Cambridge South')