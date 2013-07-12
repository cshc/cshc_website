import logging
from datetime import timedelta
from django.shortcuts import get_object_or_404
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed
from django.core.urlresolvers import reverse
from django_ical.views import ICalFeed
from core.models import not_none_or_empty
from matches.models import Match
from matches.feeds import MatchICalFeed
from .models import ClubTeam

log = logging.getLogger(__name__)



class ClubTeamMatchICalFeed(MatchICalFeed):
    """
    The iCal calendar feed for a team's matches.

    This feed returns all a team's matches for the current season. By subscribing to this feed, anyone can see all of
    a team's matches in their own calendar. As match results are entered on the Cambridge South site, their calendar 
    will reflect these updates (i.e. the calendar entry title of matches in the past will contain the match score)."
    """
    #product_id = '-//cambridgesouthhockeyclub.co.uk//Calendar 1.0//EN'
    #timezone = 'Europe/London'
    #item_class = 'PUBLIC'

    def get_object(self, request, slug):
        return get_object_or_404(ClubTeam, slug=slug)

    def title(self, obj):
        """Gets the calendar title"""
        return "CSHC %s fixtures" % obj.long_name

    def description(self, obj):
        """Gets a description of the calendar"""
        return "CSHC %s: up-to-date details of all matches for the current season, including results" % obj.long_name

    def items(self, obj):
        """Gets all the matches that make up the calendar entries"""
        return Match.objects.this_season().select_related('our_team', 'opp_team__club', 'venue').filter(our_team=obj).order_by('date')

    #def item_title(self, item):
    #    """Gets the title of a match calendar entry"""
    #    return item.fixture_title()

    #def item_link(self, item):
    #    """Gets the link/url of a match calendar entry"""
    #    return item.get_absolute_url()

    #def item_location(self, item):
    #    """Gets the location of a match calendar entry"""
    #    if item.venue_id is not None:
    #        return item.venue.full_address()
    #    else:
    #        return None

    #def item_start_datetime(self, item):
    #    """Gets the start time of a match calendar entry"""
    #    return item.datetime()

    #def item_end_datetime(self, item):
    #    """Gets the end time of a match calendar entry. 
        
    #    If the start time is known, this is 70 minutes after the start time. 
    #    Otherwise it is just the same date as the start time.
    #    """
    #    if item.time is not None:
    #        return item.datetime() + timedelta(minutes=70)
    #    else:
    #        return item.datetime()


class RssClubTeamMatchReportsFeed(Feed):

    _item_count = 10

    def title(self, obj):
       return "Cambridge South Hockey Club {} Match Reports".format(obj.long_name)

    link = "/"

    def description(self, obj):
       return "Updates when new match reports are published for Cambridge South Hockey Club {} matches.".format(obj.long_name)

    feed_copyright = "Copyright (c) 2013, Cambridge South Hockey Club"

    def get_object(self, request, slug):
        return get_object_or_404(ClubTeam, slug=slug)

    def feed_url(self, obj):
       return reverse('clubteam_match_rss_feed', args=[obj.slug])
    
    def items(self, obj):
        """ Returns the latest 10 match reports."""
        # TODO: Decide on number of reports to return
        return Match.objects.filter(our_team=obj).reports().reverse()[:RssClubTeamMatchReportsFeed._item_count]

    def item_title(self, item):
        """Returns the title of the entry"""
        return item.match_title_text()

    def item_author_name(self, item):
        """Returns the name of the author (of the match report), or None if no author specified"""
        if not_none_or_empty(item.report_author):
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