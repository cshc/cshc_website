""" A simple key-value dictionary stored in the database.
"""

from django.db import models


class ClubInfo(models.Model):
    """ This model is used as a look-up table for club information where the actual
        value may change over time and needs to be easily editable through the admin backend
        without modification to the templates or Python code that reference it.
    """

    key = models.CharField(max_length=20, unique=True)
    """ The look-up key. The value of this field is what is referenced directly in
    template and Python code."""

    value = models.CharField(max_length=100)
    """ The lookup value. This is the actual value that is required by the templates
    or Python code."""

    class Meta:
        """ Meta-info for the ClubInfo model. """
        app_label = 'core'
        verbose_name = 'Club Information'
        verbose_name_plural = 'Club Information'
        ordering = ['key']

    def __unicode__(self):
        return unicode("{}: {}".format(self.key, self.value))
