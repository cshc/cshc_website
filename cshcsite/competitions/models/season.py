import logging
from django.db import models, IntegrityError
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
        return self.slug

    def save(self, *args, **kwargs):
        # Make sure the start is before the end!
        if (self.start != None and
            self.end != None and
            self.start >= self.end):
            raise IntegrityError("The start of the season must be before the end of the season")

        # Prevent any overlapping seasons
        if Season.objects.filter(start__lte=self.start, end__gte=self.start).exists():
            raise IntegrityError("The starting date of this season overlaps with another season")
        elif Season.objects.filter(start__lte=self.end, end__gte=self.end).exists():
            raise IntegrityError("The end date of this season overlaps with another season")

        # Automatically set the slug field
        self.slug = "{}-{}".format(self.start.year, self.end.year)

        super(Season, self).save(*args, **kwargs)


    @staticmethod
    def current():
        """Returns the current season"""
        try:
            return Season.objects.by_date(datetime.now().date())
        except Season.DoesNotExist:
            log.error("Could not return current season. (Date = %s)" % datetime.now().date())
            raise

    @staticmethod
    def is_current_season(season_id):
        """Returns true if the specified season ID is the ID of the current season"""
        log.debug("Current season ID = {}".format(Season.current().pk))
        return Season.current().pk == season_id