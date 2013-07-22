import logging
from django.db import models
from django.template.defaultfilters import slugify
from core.models import TeamGender, TeamOrdinal, ordinal_from_TeamOrdinal

log = logging.getLogger(__name__)


class ClubTeamManager(models.Manager):
    """Model manager for the ClubTeam model"""

    def mens(self):
        """Returns only men's teams"""
        return self.get_query_set().filter(gender=TeamGender.mens)

    def ladies(self):
        """Returns only ladies teams"""
        return self.get_query_set().filter(gender=TeamGender.ladies)

    def m1(self):
        """Returns the Men's 1sts team"""
        return self.get_query_set().get(gender=TeamGender.mens, ordinal=TeamOrdinal.T1)

    def m2(self):
        """Returns the Men's 2nds team"""
        return self.get_query_set().get(gender=TeamGender.mens, ordinal=TeamOrdinal.T2)

    def m3(self):
        """Returns the Men's 3rds team"""
        return self.get_query_set().get(gender=TeamGender.mens, ordinal=TeamOrdinal.T3)

    def m4(self):
        """Returns the Men's 4ths team"""
        return self.get_query_set().get(gender=TeamGender.mens, ordinal=TeamOrdinal.T4)

    def l1(self):
        """Returns the Ladies 1sts team"""
        return self.get_query_set().get(gender=TeamGender.ladies, ordinal=TeamOrdinal.T1)

    def l2(self):
        """Returns the Ladies 2nds team"""
        return self.get_query_set().get(gender=TeamGender.ladies, ordinal=TeamOrdinal.T2)

    def mixed(self):
        """Return the mixed team"""
        return self.get_query_set().get(gender=TeamGender.mixed, ordinal=TeamOrdinal.T1)

    def indoor(self):
        """Return the indoor team"""
        return self.get_query_set().get(gender=TeamGender.mixed, ordinal=TeamOrdinal.TIndoor)

    def vets(self):
        """Return the vets team"""
        return self.get_query_set().get(gender=TeamGender.mens, ordinal=TeamOrdinal.TVets)


class ClubTeam(models.Model):
    """Represents a Cambridge South team"""

    short_name = models.CharField(max_length=10, unique=True)
    """A short identifying name for the team, e.g. 'M1'. Used in links etc."""

    long_name = models.CharField(max_length=100, unique=True)
    """The full name of the team, e.g. 'Men's 1st XI'"""

    gender = models.CharField("Team gender (mens/ladies)", max_length=6, choices=TeamGender)
    """The team gender (mens/ladies/mixed)"""

    ordinal = models.CharField("Team ordinal (1sts/2nds etc)", max_length=10, choices=TeamOrdinal)
    """The team ordinal (1sts/2nds/Vets/Indoor etc)"""

    position = models.PositiveSmallIntegerField(unique=True, help_text="Used to order the teams for display")
    """The position attribute is used when ordering teams in a list of teams"""

    southerners = models.BooleanField(help_text="Include in Southerners League stats", default=True)
    """If set to False, this team will not appear in the Southerners League tables"""

    rivals = models.BooleanField(help_text="Include in Rivals stats", default=True)
    """If set to False, this team's results will not count towards Rivals stats"""

    fill_blanks = models.BooleanField(help_text="Show blank fixture dates", default=True)
    """If set to True, any Saturdays in the season with no fixtures will appear as blank rows in a list of fixtures for this team"""

    personal_stats = models.BooleanField(help_text="Use for personal stats", default=True)
    """If set to False, this team's results will not count towards personal stats"""

    slug = models.SlugField("Slug")
    """Auto-generated team slug. E.g. 'mens-1st-xi'."""

    #blurb = models.TextField(blank=True)

    objects = ClubTeamManager()

    class Meta:
        app_label = 'teams'
        ordering = ['position']

    def save(self, *args, **kwargs):
        self.slug = slugify(self.short_name)
        super(ClubTeam, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.short_name

    @models.permalink
    def get_absolute_url(self):
        return ('clubteam_detail', [self.slug])

    def abbr_name(self):
        """Returns an abbreviated name, including the club (e.g. 'Cambridge South 1')"""
        return "Cambridge South {}".format(ordinal_from_TeamOrdinal(self.ordinal))
