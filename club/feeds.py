from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from datetime import datetime, date, time
from club.models import Match

class RssMatchReportsFeed(Feed):
    """ 
    Represents a feed of match reports. 
    Note: Default feed_type is RSS 2
    """

    title = "Cambridge South Hockey Club Match Reports"
    link = "/"
    feed_url = "/matches/rss/"
    description = "Updates when new match reports are published for Cambridge South Hockey Club matches."
    feed_copyright = "Copyright (c) 2013, Cambridge South Hockey Club"

    def items(self):
        """ Returns the latest 6 match reports (nominally one per team)."""
        # TODO: Decide on number of reports to return
        return Match.objects.reports().reverse()[:6]

    def item_title(self, item):
        return item.match_title_text()

    def item_author_name(self, item):
        return item.report_author

    def item_description(self, item):
        return item.report_body

    def item_pubdate(self, item):
        # TODO: This is not the published date but the actual date on which the match was played.
        #       Do we need a report_pub_date field?
        return datetime(item.date.year, item.date.month, item.date.day)


class AtomMatchReportsFeed(RssMatchReportsFeed):
    """
    Represents an Atom 1 feed of match reports.
    """

    feed_type = Atom1Feed
    feed_url = "/matches/atom/"
    subtitle = RssMatchReportsFeed.description