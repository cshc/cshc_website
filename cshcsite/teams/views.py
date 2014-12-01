""" Views relating to CSHC teams.
"""

import logging
from collections import defaultdict
from itertools import groupby
from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.conf import settings
from core.views import (kwargs_or_none, AjaxGeneral, saturdays_in_range,
                        get_season_from_kwargs, add_season_selector)
from core.stats import MatchStats
from competitions.models import Season, DivisionResult
from matches.models import Match, Appearance
from awards.models import MatchAwardWinner
from teams.stats import (SquadMember, update_southerners_stats_for_season,
                         update_participation_stats, update_participation_stats_for_season)
from teams.league_scraper import get_east_leagues_nw_division
from teams.models import ClubTeam, ClubTeamSeasonParticipation, TeamCaptaincy, Southerner

LOG = logging.getLogger(__name__)


class ClubTeamListView(TemplateView):
    """ View of a list of all CSHC teams. """

    model = ClubTeam
    template_name = 'teams/clubteam_list.html'

    def get_context_data(self, **kwargs):
        context = super(ClubTeamListView, self).get_context_data(**kwargs)

        all_teams = ClubTeam.objects.all()

        teams = {}
        teams['active'] = defaultdict(list)
        teams['inactive'] = defaultdict(list)

        for team in all_teams:
            teams['active' if team.active else 'inactive'][team.get_gender_display()].append(team)
            team_participations = ClubTeamSeasonParticipation.objects.by_team(team).order_by('-season__start')
            try:
                team.photo = team_participations[0].team_photo.url
            except:
                LOG.warn("Could not get team photo for {}".format(team))
                team.photo = settings.STATIC_URL + 'media/team_photos/placeholder_small.jpg'
            team.ical = reverse('clubteam_ical_feed', kwargs={'slug': team.slug})
            team.rss = reverse('clubteam_match_rss_feed', kwargs={'slug': team.slug})

        #(('mens', mens_teams), ('ladies', ladies_teams), ('other', other_teams))
        context['teams'] = teams
        return context


class ClubTeamDetailView(TemplateView):
    """ Details of a particular CSHC team. """

    model = ClubTeam
    template_name = 'teams/clubteam_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ClubTeamDetailView, self).get_context_data(**kwargs)

        # The team is specified in the URL by its slug
        team = get_object_or_404(ClubTeam, slug=kwargs['slug'])
        context['clubteam'] = team

        # Get the seasons in which this team competed
        part_seasons = Season.objects.filter(clubteamseasonparticipation__team=team).order_by('-start')

        # The season may or may not be specified in the URL by its slug.
        # If it isn't, we use the current season
        season_slug = kwargs_or_none('season_slug', **kwargs)
        if season_slug is not None:
            season = Season.objects.get(slug=season_slug)
        else:
            # Default to the most recent season
            season = part_seasons[0]

        # Retrieve captaincy information for this team
        context['captains'] = TeamCaptaincy.get_captains(team, season)
        context['vice_captains'] = TeamCaptaincy.get_vice_captains(team, season)

        # Get the participation information for this team and season
        participation = ClubTeamSeasonParticipation.objects.select_related('division__league', 'season').get(team=team, season=season)
        context['participation'] = participation

        add_season_selector(context, season, part_seasons)
        return context


class ClubTeamStatsView(AjaxGeneral):
    """ An Ajax-requested view for fetching all team stats for a particular season"""

    template_name = 'teams/_clubteam_stats.html'

    def get_template_context(self, **kwargs):
        context = {}

        # The team is specified in the URL by its slug
        team = ClubTeam.objects.get(slug=kwargs['slug'])
        context['clubteam'] = team

        # The season is specified in the URL by its primary key
        season_id = int(kwargs['season_pk'])
        season = Season.objects.get(pk=season_id)
        context['season'] = season
        is_current_season = Season.is_current_season(season_id)

        # Get all matches for this team and season
        match_qs = Match.objects.select_related('our_team', 'opp_team__club', 'venue',
                                                'division__league', 'cup', 'season')
        match_qs = match_qs.filter(our_team=team, season_id=season_id)

        # Get all appearances for this team and season
        app_qs = Appearance.objects.select_related('member__user', 'match__season')
        app_qs = app_qs.filter(match__season_id=season_id, match__our_team=team)

        # Get all the award winners for this team and season
        award_winners_qs = MatchAwardWinner.objects.select_related('member__user', 'match__season', 'award')
        award_winners_qs = award_winners_qs.filter(match__season_id=season_id,
                                                   match__our_team=team)

        match_lookup = {match.pk: MatchStats(match) for match in match_qs}
        squad_lookup = {}

        for app in app_qs:
            if app.member_id not in squad_lookup:
                squad_lookup[app.member_id] = SquadMember(app.member)
            squad_lookup[app.member_id].add_appearance(app)
            match_lookup[app.match_id].add_appearance(app)

        for award_winner in award_winners_qs:
            if award_winner.member_id in squad_lookup:
                squad_lookup[award_winner.member_id].add_award(award_winner.award)
            match_lookup[award_winner.match_id].add_award_winner(award_winner)

        participation = ClubTeamSeasonParticipation.objects.select_related('team').get(team=team, season_id=season_id)

        context['participation'] = participation
        context['division'] = participation.division
        # Attempt to retrieve the data from the database
        context['div_data'] = DivisionResult.objects.league_table(season=season, division=participation.division)
        if not context['div_data']:
            LOG.warn("No league table available for team {} in {}".format(team, season))

        # first build the list of list of matches by date
        matches_by_date = defaultdict(list)
        [matches_by_date[m.match.date].append(m) for m in match_lookup.itervalues()]

        if team.fill_blanks:
            # populate dates with no matches
            dates = saturdays_in_range(match_qs[0].date, match_qs[len(match_qs)-1].date)
            [matches_by_date[d] for d in dates]

        # Create a list of (date, list of matchstats) tuples
        match_tuple_list = sorted(matches_by_date.items())

        context['is_current_season'] = is_current_season
        context['match_list'] = match_tuple_list
        # TODO: Sort squad by position?
        context['squad_list'] = sorted(squad_lookup.values(), key=lambda playerstats: playerstats.member.last_name)
        context['fill_blanks'] = team.fill_blanks
        return context


class ScrapeLeagueTableView(AjaxGeneral):
    """ An Ajax-requested view for refreshing the league table data for a particular team"""

    template_name = 'teams/_league_table.html'

    def get_template_context(self, **kwargs):
        context = {}

        # The team is specified in the URL by its slug
        team = ClubTeam.objects.get(slug=kwargs['slug'])
        context['clubteam'] = team

        # The season is specified in the URL by its primary key
        season_id = int(kwargs['season_pk'])
        season = Season.objects.get(pk=season_id)
        context['season'] = season
        is_current_season = Season.is_current_season(season_id)
        context['is_current_season'] = is_current_season

        participation = ClubTeamSeasonParticipation.objects.select_related('team').filter(team=team, season_id=season_id).first()

        if participation.division_tables_url:
            context['participation'] = participation
            context['division'] = participation.division
            # Delete any existing data for this league table
            DivisionResult.objects.league_table(season=season, division=participation.division).delete()
            try:
                context['div_data'] = get_east_leagues_nw_division(participation.division_tables_url, participation.division, season)
            except Exception as e:
                print "Failed to parse league table: {}".format(e)
        return context

###############################################################################
# SOUTHERNERS LEAGUE


class SouthernersMixin(object):
    """ Provides useful methods for Southerners League views"""

    def get_southerners_list(self, season):
        """ Returns a list of Southerners League items for the specified season"""

        # We convert the queryset to a list so we can add a 'rank' attribute to each item
        team_list = list(Southerner.objects.by_season(season))

        # Apply ranking
        if len(team_list) > 0:
            rank = 1
            previous = team_list[0]
            previous.rank = 1
            for i, entry in enumerate(team_list[1:]):
                if entry.avg_points_per_game != previous.avg_points_per_game:
                    rank = i + 2
                    entry.rank = str(rank)
                else:
                    entry.rank = "%s=" % rank
                    previous.rank = entry.rank
                previous = entry

        return team_list


class SouthernersSeasonView(SouthernersMixin, TemplateView):
    """ View for displaying the Southerners League stats for a particular season"""

    template_name = 'teams/southerners_league.html'

    def get_context_data(self, **kwargs):
        """ Gets the context data for the view.

            In addition to the 'team_list' item, the following are also added to the context:
            - season:               the season these stats applies to
            - season_list:          a list of all seasons
            - is_current_season:    True if season == Season.current()
        """
        context = super(SouthernersSeasonView, self).get_context_data(**kwargs)
        season = get_season_from_kwargs(kwargs)

        context['team_list'] = self.get_southerners_list(season)

        add_season_selector(context, season, Season.objects.reversed())

        return context


class SouthernersSeasonUpdateView(SouthernersMixin, AjaxGeneral):
    """ View for updating and then displaying Southerners Leauge stats for a particular season"""

    template_name = 'teams/_southerners_league_table.html'

    def get_template_context(self, **kwargs):
        """ Updates the Southerners Leauge stats for the specified season and then returns
            the context data for the template, containing just a 'team_list' item
        """
        # The season_slug keyword arg should always be supplied to this view
        season = Season.objects.get(slug=kwargs['season_slug'])
        update_southerners_stats_for_season(season)

        return {'team_list': self.get_southerners_list(season)}



class ParticipationUpdateView(AjaxGeneral):
    """ View for updating and then displaying Club Team stats for a
        particular season
    """

    template_name = 'teams/_participation_stats.html'

    def get_template_context(self, **kwargs):
        """ Updates the Club Team stats for the specified season and then returns
            the context data for the template, containing just a 'participation' item
        """
        # The season_slug keyword arg should always be supplied to this view
        participation = ClubTeamSeasonParticipation.objects.get(pk=int(kwargs['participation_id']))
        update_participation_stats(participation)

        return {'participation': participation}


###############################################################################
# PLAYING RECORD


class PlayingRecordMixin(object):
    """ Provides useful methods for Playing Record views"""

    def get_all_playing_records(self):
        """ Returns a dictionary of Playing Records, keyed by team """

        # Get all participation entries
        participations = ClubTeamSeasonParticipation.objects.all().select_related('team', 'season').order_by('team', '-season')

        grouped_by_team = groupby(participations, lambda x: x.team)
        parts = {}
        for team, seasons in grouped_by_team:
            print team.long_name
            parts[team] = []
            for participation in seasons:
                print "\t{}".format(participation.season)
                parts[team].append(participation)

        return parts


class PlayingRecordView(PlayingRecordMixin, TemplateView):
    """ View of the playing record stats for each team in the club"""

    template_name = 'teams/playing_record.html'

    def get_context_data(self, **kwargs):
        context = super(PlayingRecordView, self).get_context_data(**kwargs)
        context['participation'] = self.get_all_playing_records()
        return context


class PlayingRecordUpdateView(PlayingRecordMixin, AjaxGeneral):
    """ View for updating and then displaying Playing Record stats for all teams """

    template_name = 'teams/_playing_record_table.html'

    def get_template_context(self, **kwargs):
        """ Updates the Playing Record stats for all teams and all seasons and then returns
            the context data for the template.
        """
        for season in Season.objects.all():
            update_participation_stats_for_season(season)

        return {'participation': self.get_all_playing_records()}
