import logging
from django.shortcuts import get_object_or_404
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.conf import settings
from core.models import not_none_or_empty
from matches.models import Match
from matches.feeds import MatchICalFeed, ImageRssFeedGenerator
from .models import ClubTeam

log = logging.getLogger(__name__)



class ClubTeamMatchICalFeed(MatchICalFeed):
    """
    The iCal calendar feed for a team's matches.

    This feed returns all a team's matches for the current season. By subscribing to this feed, anyone can see all of
    a team's matches in their own calendar. As match results are entered on the Cambridge South site, their calendar
    will reflect these updates (i.e. the calendar entry title of matches in the past will contain the match score)."
    """

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
        return Match.objects.this_season().select_related('our_team', 'opp_team__club', 'venue').filter(our_team=obj).order_by('date', 'time')


class RssClubTeamMatchReportsFeed(Feed):

    _item_count = 10
    feed_type = ImageRssFeedGenerator

    def title(self, obj):
       return "Cambridge South Hockey Club {} Match Reports".format(obj.long_name)

    link = "http://" + Site.objects.all()[0].domain
    icon = settings.STATIC_URL + 'ico/favicon.ico'

    def description(self, obj):
       return "Updates when new match reports are published for Cambridge South Hockey Club {} matches.".format(obj.long_name)

    feed_copyright = "Copyright (c) 2013, Cambridge South Hockey Club"

    def feed_extra_kwargs(self, obj):
        return {'image_url': settings.STATIC_URL + 'media/crest.png'}

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
        """Returns the date the match report was first published"""
        return item.report_pub_timestamp