""" The ClubTeam model represents a Cambridge South team.
"""

from django.db import models
from django.template.defaultfilters import slugify
from django.db.models.query import QuerySet
from model_utils.managers import PassThroughManager
from core.models import TeamGender, TeamOrdinal, ordinal_from_TeamOrdinal


class ClubTeamQuerySet(QuerySet):
    """ Queries relating to the ClubTeam model"""

    def active(self):
        """ Returns only active teams (currently playing)"""
        return self.filter(active=True)

    def mens(self):
        """ Returns only men's teams"""
        return self.filter(gender=TeamGender.Mens)

    def ladies(self):
        """ Returns only ladies teams"""
        return self.filter(gender=TeamGender.Ladies)

    def m1(self):
        """ Returns the Men's 1sts team"""
        return self.get(gender=TeamGender.Mens, ordinal=TeamOrdinal.T1)

    def m2(self):
        """ Returns the Men's 2nds team"""
        return self.get(gender=TeamGender.Mens, ordinal=TeamOrdinal.T2)

    def m3(self):
        """ Returns the Men's 3rds team"""
        return self.get(gender=TeamGender.Mens, ordinal=TeamOrdinal.T3)

    def m4(self):
        """ Returns the Men's 4ths team"""
        return self.get(gender=TeamGender.Mens, ordinal=TeamOrdinal.T4)

    def l1(self):
        """ Returns the Ladies 1sts team"""
        return self.get(gender=TeamGender.Ladies, ordinal=TeamOrdinal.T1)

    def l2(self):
        """ Returns the Ladies 2nds team"""
        return self.get(gender=TeamGender.Ladies, ordinal=TeamOrdinal.T2)

    def l3(self):
        """ Returns the Ladies 3rds team"""
        return self.get(gender=TeamGender.Ladies, ordinal=TeamOrdinal.T3)

    def l4(self):
        """ Returns the Ladies 4ths team"""
        return self.get(gender=TeamGender.Ladies, ordinal=TeamOrdinal.T4)

    def l5(self):
        """ Returns the Ladies 5ths team"""
        return self.get(gender=TeamGender.Ladies, ordinal=TeamOrdinal.T5)

    def mixed(self):
        """ Return the mixed team"""
        return self.get(gender=TeamGender.Mixed, ordinal=TeamOrdinal.TOther)

    def indoor(self):
        """ Return the indoor team"""
        return self.get(gender=TeamGender.Mixed, ordinal=TeamOrdinal.TIndoor)

    def vets(self):
        """ Return the vets team"""
        return self.get(gender=TeamGender.Mens, ordinal=TeamOrdinal.TVets)


class ClubTeam(models.Model):
    """ Represents a Cambridge South team"""

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

    active = models.BooleanField(help_text="Uncheck if this team is not currently active", default=True)
    """If set to False, this team will be hidden from items like Latest Results and team lists."""

    slug = models.SlugField("Slug")
    """Auto-generated team slug. E.g. 'mens-1st-xi'."""

    blurb = models.TextField(blank=True)
    """ Some current detail about the team. """

    google_calendar_url = models.CharField("Google Calendar Feed URL", max_length=200, help_text="\
    The URL of the Google Calendar feed for this team.\
    \
    When a new team is added, a new Google Calendar feed is created by pointing Google Calendar \
    at the team's ical URL (the 'clubteam_ical_feed' url). The Google Calendar feed URL generated \
    from this is what should go in this field.", blank=True)
    """
    The URL of the Google Calendar feed for this team.

    When a new team is added, a new Google Calendar feed is created by pointing Google Calendar
    at the team's ical URL (the 'clubteam_ical_feed' url). The Google Calendar feed URL generated
    from this is what should go in this field.

    Login to google calendar (email address and password in 'Account Details' Google Doc)
    to get these addresses.
    """

    objects = PassThroughManager.for_queryset_class(ClubTeamQuerySet)()

    class Meta:
        """ Meta-info for the ClubTeam model. """
        app_label = 'teams'
        ordering = ['position']

    def clean(self):
        self.slug = slugify(self.short_name)

    def __unicode__(self):
        return unicode(self.short_name)

    @models.permalink
    def get_absolute_url(self):
        """ Returns the URL for this ClubTeam instance. """
        return ('clubteam_detail', [self.slug])

    def abbr_name(self):
        """ Returns an abbreviated name, including the club (e.g. 'Cambridge South 1')"""
        if self.short_name in ['Mixed', 'Indoor']:
            return "Cambridge South {}".format(self.short_name)
        elif self.gender == TeamGender.Ladies:
            return "Cambridge South Ladies {}".format(ordinal_from_TeamOrdinal(self.ordinal))
        else:
            return "Cambridge South Mens {}".format(ordinal_from_TeamOrdinal(self.ordinal))

    def genderless_abbr_name(self):
        """ Returns the abbreviated team name without either 'Ladies' or 'Mens'. """
        return self.abbr_name().replace(" Ladies", "").replace(" Mens", "")
