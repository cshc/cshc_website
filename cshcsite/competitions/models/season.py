import logging
from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime

log = logging.getLogger(__name__)


class SeasonManager(models.Manager):
    """Model Manager for Season models"""

    def by_date(self, date):
        """Returns the season in which the specified date falls"""
        return super(SeasonManager, self).get_query_set().get(start__lte=date, end__gte=date)


class Season(models.Model):
    """Represents a season during which matches are played"""

    # The first date of the season
    start = models.DateField("Season start", help_text="(Approx) first day of the season")

    # The last date of the season
    end = models.DateField("Season end", help_text="(Approx) last day of the season")

    # A slug to identify the season. This will be automatically created
    slug = models.SlugField()

    objects = SeasonManager()

    class Meta:
        app_label = 'competitions'
        ordering = ['start']
        get_latest_by = "start"

    def __unicode__(self):
        return unicode(self.slug)
    __unicode__.short_description = 'Season'

    def clean(self):
        # Make sure the start is before the end!
        if (self.start is not None and self.end is not None and self.start >= self.end):
            raise ValidationError("The start of the season must be before the end of the season")

        # Prevent any overlapping seasons
        if Season.objects.exclude(pk=self.pk).filter(start__lte=self.start, end__gte=self.start).exists():
            raise ValidationError("The starting date of this season overlaps with another season")
        elif Season.objects.exclude(pk=self.pk).filter(start__lte=self.end, end__gte=self.end).exists():
            raise ValidationError("The end date of this season overlaps with another season")

        # Automatically set the slug field
        self.slug = "{}-{}".format(self.start.year, self.end.year)

    @staticmethod
    def current():
        """Returns the current season"""
        try:
            return Season.objects.by_date(datetime.now().date())
        except Season.DoesNotExist:
            log.warn("Current season not found. Creating now")
            return Season.create_current_season()

    @staticmethod
    def is_current_season(season_id):
        """Returns true if the specified season ID is the ID of the current season"""
        log.debug("Current season ID = {}".format(Season.current().pk))
        return Season.current().pk == season_id

    @staticmethod
    def create_current_season():
        current = Season()
        dt = datetime.now()
        if dt.month >= 9:
            start_year = dt.year
        else:
            start_year = dt.year - 1

        current.start = datetime(year=start_year, month=9, day=1)
        current.end = datetime(year=start_year+1, month=8, day=31)
        current.save()
        return current
