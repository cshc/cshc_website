import logging
from datetime import timedelta
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.core.urlresolvers import reverse
from core.models import not_none_or_empty
from django_ical.views import ICalFeed
from .models import Match

log = logging.getLogger(__name__)


class RssMatchReportsFeed(Feed):
    """
    Represents a feed of match reports.
    Note: Default feed_type is RSS 2
    """

    _item_count = 10

    title = "Cambridge South Hockey Club Match Reports"
    link = "/"
    description = "Updates when new match reports are published for Cambridge South Hockey Club matches."
    feed_copyright = "Copyright (c) 2013, Cambridge South Hockey Club"

    def feed_url(self):
       return reverse('match_report_rss_feed')

    def items(self):
        """ Returns the latest 10 match reports."""
        # TODO: Decide on number of reports to return
        return Match.objects.reports().reverse()[:RssMatchReportsFeed._item_count]

    def item_title(self, item):
        """Returns the title of the entry"""
        return "[{}] {}".format(item.home_away_abbrev(), item.match_title_text())

    def item_author_name(self, item):
        """Returns the name of the author (of the match report), or None if no author specified"""
        if item.report_author:
            return item.report_author.full_name()
        return None

    def item_description(self, item):
        """Returns the item description - the actual match report"""
        return item.report_body

    def item_pubdate(self, item):
        """Currently returns the date of the match itself (not actually when the report was 'published')"""
        # TODO: This is not the published date but the actual date on which the match was played.
        #       Do we need a report_pub_date field?
        return item.datetime()


class AtomMatchReportsFeed(RssMatchReportsFeed):
    """
    Represents an Atom 1 feed of match reports.
    """

    feed_type = Atom1Feed
    subtitle = RssMatchReportsFeed.description

    def feed_url(self):
       return reverse('match_report_atom_feed')



class MatchICalFeed(ICalFeed):
    """
    The iCal calendar feed for all matches.

    This feed returns all matches for the current season. By subscribing to this feed, anyone can see all CSHC matches
    in their own calendar. As match results are entered on the Cambridge South site, their calendar
    will reflect these updates (i.e. the calendar entry title of matches in the past will contain the match score)."
    """
    product_id = '-//cambridgesouthhockeyclub.co.uk//Calendar 1.0//EN'
    timezone = 'Europe/London'
    item_class = 'PUBLIC'

    title = "CSHC fixtures"
    description = "Up-to-date details of all CSHC matches for the current season, including results"

    def items(self):
        """Gets all the matches that make up the calendar entries"""
        return Match.objects.this_season().select_related('our_team', 'opp_team__club', 'venue').order_by('date')

    def item_title(self, item):
        """Gets the title of a match calendar entry"""
        return item.fixture_title()

    def item_link(self, item):
        """Gets the link/url of a match calendar entry"""
        return item.get_absolute_url()

    def item_location(self, item):
        """Gets the location of a match calendar entry"""
        if item.venue_id is not None:
            return "{}, {}".format(item.venue.name, item.venue.full_address())
        else:
            return None

    def item_start_datetime(self, item):
        """Gets the start time of a match calendar entry"""
        return item.datetime()

    def item_end_datetime(self, item):
        """Gets the end time of a match calendar entry.

        If the start time is known, this is 70 minutes after the start time.
        Otherwise it is just the same date as the start time.
        """
        if item.time is not None:
            return item.datetime() + timedelta(minutes=70)
        else:
            return item.datetime()

