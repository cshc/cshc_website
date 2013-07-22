import logging
from django.db import models
from django.template.defaultfilters import slugify
from core.models import TeamGender
from club import Club

log = logging.getLogger(__name__)


class TeamManager(models.Manager):
    """Model manager for the Team model"""

    def mens(self):
        """Returns only men's teams"""
        return self.get_query_set().filter(gender=TeamGender.mens)

    def ladies(self):
        """Returns only ladies teams"""
        return self.get_query_set().filter(gender=TeamGender.ladies)

    def mixed(self):
        """Returns only mixed teams"""
        return self.get_query_set().filter(gender=TeamGender.mixed)


class Team(models.Model):
    """Represents an opposition team"""

    # The club this team is a part of
    club = models.ForeignKey(Club, related_name="teams")

    # Full name of the team
    name = models.CharField("Team name", max_length=100, unique=True)

    # Abbreviated name of the team
    short_name = models.CharField("Abbreviated name", max_length=100)

    # Mens/ladies/mixed team
    gender = models.CharField("Team gender (mens/ladies)", max_length=6, choices=TeamGender)

    # Auto-generated slug
    slug = models.SlugField("Slug")

    objects = TeamManager()

    class Meta:
        app_label = 'opposition'
        ordering = ['club', 'name']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Team, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return ('opposition_team_detail', [self.slug])
