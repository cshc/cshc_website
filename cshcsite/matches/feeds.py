""" The code in this module auto-generates RSS/Atom feeds for
    matches played by CSHC teams. There is a general one for all
    teams as well as team-specific feeds.

    Ref: https://docs.djangoproject.com/en/1.6/ref/contrib/syndication/

    Additionally there is an automatically generated calendar feed
    for matches this season.

    This feed can be added to an external calendar app to display all
    training sessions.

    Ref: http://django-ics.readthedocs.org/en/latest/usage.html#overview
"""

from datetime import timedelta
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed, Rss201rev2Feed
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.conf import settings
from django_ical.views import ICalFeed
from matches.models import Match


class ImageRssFeedGenerator(Rss201rev2Feed):
    """ A feed generator that incorporates an image. """

    def add_root_elements(self, handler):
        super(ImageRssFeedGenerator, self).add_root_elements(handler)
        handler.startElement(u'image', {})
        handler.addQuickElement(u"url", self.feed['image_url'])
        handler.addQuickElement(u"title", self.feed['title'])
        handler.addQuickElement(u"link", self.feed['link'])
        handler.addQuickElement(u"width", '100')
        handler.addQuickElement(u"height", '100')
        handler.endElement(u'image')


class RssMatchReportsFeed(Feed):
    """ Represents a feed of match reports.
        Note: Default feed_type is RSS 2
    """

    _item_count = 7*4   # Approx four weeks for 7 teams
    feed_type = ImageRssFeedGenerator
    title = "Cambridge South Hockey Club Match Reports"
    link = "http://" + Site.objects.all()[0].domain
    description = "Updates when new match reports are published for Cambridge South Hockey Club matches."
    feed_copyright = "Copyright (c) 2015, Cambridge South Hockey Club"
    icon = settings.STATIC_URL + 'ico/favicon.ico'

    def feed_extra_kwargs(self, obj):
        return {'image_url': settings.STATIC_URL + 'media/crest.png'}

    def feed_url(self):
        """ Returns the url for this feed."""
        return reverse('match_report_rss_feed')

    def items(self):
        """ Returns the latest match reports."""
        return Match.objects.reports().reverse()[:RssMatchReportsFeed._item_count]

    def item_link(self, item):
        """ Gets the link/url of a match report entry"""
        return item.get_absolute_url()

    def item_title(self, item):
        """ Returns the title of the entry"""
        return item.match_title_text()

    def item_author_name(self, item):
        """ Returns the name of the author (of the match report), or
            None if no author specified.
        """
        if item.report_author:
            return item.report_author.full_name()
        return None

    def item_description(self, item):
        """ Returns the item description - the actual match report"""
        return item.report_body

    def item_pubdate(self, item):
        """ Returns the date the match report was first published"""
        return item.report_pub_timestamp


class AtomMatchReportsFeed(RssMatchReportsFeed):
    """ Represents an Atom 1 feed of match reports.
    """

    feed_type = Atom1Feed
    subtitle = RssMatchReportsFeed.description

    def feed_url(self):
        return reverse('match_report_atom_feed')



class MatchICalFeed(ICalFeed):
    """ The iCal calendar feed for all matches.

        This feed returns all matches for the current season. By subscribing to
        this feed, anyone can see all CSHC matches in their own calendar. As match
        results are entered on the Cambridge South site, their calendar will
        reflect these updates (i.e. the calendar entry title of matches in the
        past will contain the match score)."
    """
    product_id = '-//cambridgesouthhockeyclub.co.uk//Calendar 1.0//EN'
    timezone = 'Europe/London'
    item_class = 'PUBLIC'

    title = "CSHC fixtures"
    description = "Up-to-date details of all CSHC matches for the current season, including results"

    def items(self):
        """ Gets all the matches that make up the calendar entries"""
        return Match.objects.this_season().select_related('our_team', 'opp_team__club', 'venue').order_by('date', 'time')

    def item_description(self, item):
        """ Returns the item description - the actual match report"""
        return item.match_title_text()

    def item_title(self, item):
        """ Gets the title of a match calendar entry"""
        return "[{}] {}".format(item.home_away_abbrev(), item.fixture_title())

    def item_link(self, item):
        """ Gets the link/url of a match calendar entry"""
        return item.get_absolute_url()

    def item_location(self, item):
        """ Gets the location of a match calendar entry"""
        if item.venue_id is not None:
            return "{}, {}".format(item.venue.name, item.venue.full_address())
        else:
            return None

    def item_start_datetime(self, item):
        """ Gets the start time of a match calendar entry"""
        if item.time is not None:
            return item.datetime()
        else:
            return item.date

    def item_end_datetime(self, item):
        """ Gets the end time of a match calendar entry.

            If the start time is known, this is 90 minutes after the start time.
            Otherwise it is just the same date as the start time.
        """
        if item.time is not None:
            return item.datetime() + timedelta(minutes=90)
        else:
            return item.date

