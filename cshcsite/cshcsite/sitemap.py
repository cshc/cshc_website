"""
    This module defines the sitemaps for ALL apps in the CSHC website.
    Ref: https://docs.djangoproject.com/en/1.6/ref/contrib/sitemaps/

    The sitemap is split into sections, each of which is referenced by
    the sitemap index. See definition of 'CshcSitemap' below for details.
"""

from django.contrib.sitemaps import Sitemap, FlatPageSitemap
from django.core.urlresolvers import reverse
from zinnia.sitemaps import TagSitemap
from zinnia.sitemaps import EntrySitemap
from zinnia.sitemaps import CategorySitemap
from zinnia.sitemaps import AuthorSitemap
from matches.models import Match
from competitions.models import Season
from members.models import Member
from opposition.models import Club
from teams.models import ClubTeam, ClubTeamSeasonParticipation
from training.models import TrainingSession
from venues.models import Venue


class SeasonalSitemap(Sitemap):
    """ Utility abstract sitemap class.

        Derived classes must provide a url_name method.
    """
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return Season.objects.all()

    def location(self, item):
        return reverse(self.url_name(), args=[item.slug])


###############################################################################
# GENERAL

class MainStaticViewSitemap(Sitemap):
    """ High-priority static pages. """
    priority = 1.0
    changefreq = 'monthly'

    def items(self):
        return [
            'homepage', 'about_us', 'calendar', 'contact_us', 'commission', 'members_offers',
            'directions', 'about_social', 'about_kit', 'about_fees', 'stats', 'user_profile',
            'registration_register', 'member_list', 'clubteam_list',
            'upcoming_trainingsession_list', 'venue_list',
        ]

    def location(self, item):
        return reverse(item)


class ArchiveStaticViewSitemap(Sitemap):
    """ Low priority (archive) static pages. """
    priority = 0.6
    changefreq = 'never'

    def items(self):
        return [
            'about_minutes',
        ]

    def location(self, item):
        return reverse(item)


class CommitteeSitemap(SeasonalSitemap):
    """ Sitemap of committee pages through the years. """

    def priority(self, item):
        if item == Season.current():
            return 1.0
        else:
            return 0.7

    def changefreq(self, item):
        if item == Season.current():
            return 'monthly'
        else:
            return 'never'

    def url_name(self):
        return 'about_committee_season'


class StatsSitemap(Sitemap):
    """ Sitemap of various stats pages. """
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return [
            'naughty_step', 'opposition_club_list', 'playing_record',
        ]

    def location(self, item):
        return reverse(item)

###############################################################################
# MATCHES

class MatchSummarySitemap(Sitemap):
    """ Sitemap of general match summary pages. """
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return [
            'match_list', 'latest_results', 'next_fixtures',
        ]

    def location(self, item):
        return reverse(item)


class MatchesBySeasonSitemap(SeasonalSitemap):
    """ Sitemap of the match summaries for each season. """
    priority = 0.5
    changefreq = 'weekly'

    def url_name(self):
        return 'matches_by_season'


class GoalKingSitemap(SeasonalSitemap):
    """ Sitemap of the goal king pages for each season. """
    priority = 0.5
    changefreq = 'weekly'

    def url_name(self):
        return 'goal_king_season'


class AccidentalTouristSitemap(SeasonalSitemap):
    """ Sitemap of the accidental tourist pages for each season. """
    priority = 0.5
    changefreq = 'weekly'

    def url_name(self):
        return 'accidental_tourist_season'


class MatchDetailSitemap(Sitemap):
    """ Sitemap of each match details page. """
    priority = 0.5
    changefreq = "weekly"

    def items(self):
        return Match.objects.all()

    def lastmod(self, obj):
        return obj.report_pub_timestamp


###############################################################################
# MEMBERS

class MemberDetailSitemap(Sitemap):
    """ Sitemap of each member details page. """
    priority = 0.5
    changefreq = "monthly"

    def items(self):
        return Member.objects.all()


###############################################################################
# OPPOSITION

class OppositionClubDetailSitemap(Sitemap):
    """ Sitemap of each opposition club details page. """
    priority = 0.3
    changefreq = "monthly"

    def items(self):
        return Club.objects.all()


###############################################################################
# TEAMS

class SouthernersSitemap(SeasonalSitemap):
    """ Sitemap of the Southerners stats pages for each season. """
    priority = 0.5
    changefreq = 'weekly'

    def url_name(self):
        return 'southerners_league_season'

class ClubTeamDetailSitemap(Sitemap):
    """ Sitemap of all the club team's details pages (default view)"""
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return ClubTeam.objects.all()

class ClubTeamArchiveSitemap(Sitemap):
    """ Sitemap of all the club team's details pages for all seasons. """
    priority = 0.5
    changefreq = 'never'

    def items(self):
        teams = ClubTeam.objects.all()
        items = []
        for team in teams:
            seasons = Season.objects.filter(clubteamseasonparticipation__team=team)
            for season in seasons:
                items.append((team.slug, season.slug))
        return items

    def location(self, item):
        return reverse('clubteam_season_detail', args=[item[0], item[1]])


###############################################################################
# TRAINING

class TrainingDetailSitemap(Sitemap):
    """ Sitemap of all the training session details pages. """
    priority = 0.4
    changefreq = 'weekly'

    def items(self):
        return TrainingSession.objects.all()


###############################################################################
# VENUES

class VenueDetailSitemap(Sitemap):
    """ Sitemap of all the venue details pages. """
    priority = 0.5
    changefreq = 'yearly'

    def items(self):
        return Venue.objects.all()



# Dictionary of sitemap sections to Sitemap classes
# Note: We're using an index so each sitemap section can be
# found at /sitemap-<section>.xml
CshcSitemap = {
    'flatpages': FlatPageSitemap,
    'match-detail': MatchDetailSitemap,
    'match-summary': MatchSummarySitemap,
    'matches-by-season': MatchesBySeasonSitemap,
    'goal-king': GoalKingSitemap,
    'accidental-tourist': AccidentalTouristSitemap,
    'members': MemberDetailSitemap,
    'opposition': OppositionClubDetailSitemap,
    'main': MainStaticViewSitemap,
    'archive': ArchiveStaticViewSitemap,
    'committee': CommitteeSitemap,
    'stats': StatsSitemap,
    'southerners': SouthernersSitemap,
    'teams': ClubTeamDetailSitemap,
    'teams-archive': ClubTeamArchiveSitemap,
    'training': TrainingDetailSitemap,
    'venues': VenueDetailSitemap,

    # Zinnia Blog - ref: http://django-blog-zinnia.readthedocs.org/en/latest/getting-started/configuration.html#module-zinnia.sitemaps
    'tags': TagSitemap,
    'blog': EntrySitemap,
    'authors': AuthorSitemap,
    'categories': CategorySitemap,
}
