import logging
from collections import defaultdict
from datetime import datetime
from django.views.generic import ListView, TemplateView
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from core.views import AjaxGeneral, saturdays_in_range

from core.models import TeamGender, first_or_none, not_none_or_empty
from core.views import kwargs_or_none
from core.stats import MatchStats
from competitions.models import Division, Season
from matches.models import Match, Appearance
from awards.models import MatchAwardWinner, MatchAward
from members.models import Member
from .stats import SquadMember, update_clubstats_for_season
from .league_scraper import get_east_leagues_nw_division, get_old_east_leagues_division, get_old_east_leagues_nw_division, get_east_leagues_cambs_division
from .models import ClubTeam, ClubTeamSeasonParticipation, TeamCaptaincy, Southerner

log = logging.getLogger(__name__)


class ClubTeamListView(TemplateView):
    """View of a list of ClubTeams"""

    model = ClubTeam
    template_name = 'teams/clubteam_list.html'

    def get_context_data(self, **kwargs):
        context = super(ClubTeamListView, self).get_context_data(**kwargs)

        all_teams = ClubTeam.objects.all()

        mens_teams = list(all_teams.filter(gender=TeamGender.mens))
        ladies_teams = list(all_teams.filter(gender=TeamGender.ladies))
        other_teams = list(all_teams.filter(gender=TeamGender.mixed))

        for team in mens_teams + ladies_teams + other_teams:
            try:
                team.photo = ClubTeamSeasonParticipation.objects.current().by_team(team)[0].team_photo.url
            except:
                log.warn("Could not get team photo for {}".format(team))
                team.photo = '/media/team_photos/placeholder_small.jpg'  # TODO: Team photo placeholder
            team.blurb = 'Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque ' + \
                         'laudantium, totam rem aperiam, eaque ipsa quae ab illo inventore veritatis et quasi ' + \
                         'architecto beatae vitae dicta sunt explicabo. Nemo enim ipsam voluptatem quia voluptas ' + \
                         'sit aspernatur aut odit aut fugit, sed quia consequuntur magni dolores eos qui ratione ' + \
                         'voluptatem sequi nesciunt.'
            team.ical = reverse('clubteam_ical_feed', kwargs={'slug': team.slug})
            team.rss = reverse('clubteam_match_rss_feed', kwargs={'slug': team.slug})

        context['teams'] = (('mens', mens_teams), ('ladies', ladies_teams), ('other', other_teams))
        return context


class ClubTeamDetailView(TemplateView):
    """View of a particular ClubTeam"""

    model = ClubTeam
    template_name = 'teams/clubteam_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ClubTeamDetailView, self).get_context_data(**kwargs)

        # The team is specified in the URL by its slug
        team = get_object_or_404(ClubTeam, slug=kwargs['slug'])
        context['clubteam'] = team

        # Get the seasons in which this team competed
        part_seasons = [part.season for part in ClubTeamSeasonParticipation.objects.select_related('season').filter(team=team).only('season').order_by('season__start')]

        # The season may or may not be specified in the URL by its slug.
        # If it isn't, we use the current season
        season_slug = kwargs_or_none('season_slug', **kwargs)
        current_season = Season.current()
        if season_slug is not None:
            season = Season.objects.get(slug=season_slug)
        else:
            # Default to the most recent season
            season = part_seasons[-1]

        # Retrieve captaincy information for this team
        context['captain'] = TeamCaptaincy.get_captain(team, season)
        context['vice_captain'] = TeamCaptaincy.get_vice_captain(team, season)

        # Get the participation information for this team and season
        participation = ClubTeamSeasonParticipation.objects.select_related('division__league', 'season').get(team=team, season=season)
        context['participation'] = participation

        # Allow the template to display the season and a season selector
        context['season'] = season
        context['season_list'] = part_seasons
        context['is_current_season'] = season == current_season
        return context


class ClubTeamStatsView(AjaxGeneral):
    """An Ajax-requested view for fetching all team stats for a particular season"""
    template_name = 'teams/_clubteam_stats.html'

    def get_template_context(self, **kwargs):
        context = {}

        # The team is specified in the URL by its slug
        team_slug = kwargs['slug']
        team = ClubTeam.objects.get(slug=team_slug)

        # The season is specified in the URL by its primary key
        season_id = int(kwargs['season_pk'])
        season = Season.objects.get(pk=season_id)
        is_current_season = Season.is_current_season(season_id)

        # Get all matches for this team and season
        matches = Match.objects.select_related('our_team', 'opp_team__club', 'venue', 'division__league', 'cup', 'season').filter(our_team__slug=team_slug, season_id=season_id).order_by('date')

        # Get all appearances for this team and season
        appearances = Appearance.objects.select_related('member__user', 'match__season').filter(match__season_id=season_id, match__our_team__slug=team_slug)

        # Get all the award winners for this team and season
        award_winners = MatchAwardWinner.objects.select_related('member__user', 'match__season', 'award').filter(match__season_id=season_id, match__our_team__slug=team_slug)

        match_lookup = {match.pk: MatchStats(match) for match in matches}
        squad_lookup = {}

        for app in appearances:
            if not squad_lookup.has_key(app.member_id):
                squad_lookup[app.member_id] = SquadMember(app.member)
            squad_lookup[app.member_id].add_appearance(app)
            match_lookup[app.match_id].add_appearance(app)

        for award_winner in award_winners:
            squad_lookup[award_winner.member_id].add_award(award_winner.award)
            match_lookup[award_winner.match_id].add_award_winner(award_winner)

        # Scrape the league table if we've got a link to the league table
        participation = first_or_none(ClubTeamSeasonParticipation.objects.select_related('team').filter(team__slug=team_slug, season_id=season_id, division_tables_url__isnull=False))

        if participation is not None and not_none_or_empty(participation.division_tables_url):
                context['participation'] = participation
                # TODO: Currently this is fairly 'hard-coded'. If a team moves out of these divisions, this code
                # will need to be modified.
                if participation.division.gender == TeamGender.mens:
                    if is_current_season:
                        context['division'] = get_east_leagues_nw_division(participation.division_tables_url, participation.division.name)
                    elif season.start < datetime(2003, 12, 01).date():
                        context['division'] = get_old_east_leagues_nw_division(participation.division_tables_url, participation.division.name)
                    else:
                        context['division'] = get_old_east_leagues_division(participation.division_tables_url, participation.division.name)
                elif participation.division.gender == TeamGender.ladies:
                    context['division'] = get_east_leagues_cambs_division(participation.division_tables_url)
                else:
                    log.warn("No league table to be scraped for team {}".format(participation.team.abbr_name()))
        else:
            log.warn("No league table link for {} in season {}".format(team_slug, season_id))

        # first build the list of list of matches by date
        matches_by_date = defaultdict(list)
        [matches_by_date[m.match.date].append(m) for m in match_lookup.itervalues()]

        if team.fill_blanks:
            # populate dates with no matches
            dates = saturdays_in_range(matches[0].date, matches[len(matches)-1].date)
            [matches_by_date[d] for d in dates]

        # Create a list of (date, list of matchstats) tuples
        match_tuple_list = sorted(matches_by_date.items())

        context['team'] = team
        context['is_current_season'] = is_current_season
        context['match_list'] = match_tuple_list
        # TODO: Sort squad by position?
        context['squad_list'] = sorted(squad_lookup.values(), key=lambda playerstats: playerstats.member.last_name)
        context['fill_blanks'] = team.fill_blanks
        return context

###############################################################################
# SOUTHERNERS LEAGUE


class SouthernersMixin(object):
    """Provides useful methods for Southerners League views"""
    def get_southerners_list(self, season):
        """Returns a list of Southerners League items for the specified season"""

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
    """View for displaying the Southerners League stats for a particular season"""
    template_name = 'teams/southerners_league.html'

    def get_context_data(self, **kwargs):
        """
        Gets the context data for the view.

        In addition to the 'team_list' item, the following are also added to the context:
            - season:               the season these stats applies to
            - season_list:          a list of all seasons
            - is_current_season:    True if season == Season.current()
        """
        context = super(SouthernersSeasonView, self).get_context_data(**kwargs)

        # If we're viewing this season's stats we may not have a season_slug keyword arg.
        season_slug = kwargs_or_none('season_slug', **kwargs)
        if season_slug is not None:
            season = Season.objects.get(slug=season_slug)
        else:
            season = Season.current()

        context['team_list'] = self.get_southerners_list(season)

        context['season'] = season
        context['is_current_season'] = season == Season.current()
        context['season_list'] = Season.objects.all()
        return context


class SouthernersSeasonUpdateView(SouthernersMixin, AjaxGeneral):
    """View for updating and then displaying Southerners Leauge stats for a particular season"""
    template_name = 'teams/_southerners_league_table.html'

    def get_template_context(self, **kwargs):
        """
        Updates the Southerners Leauge stats for the specified season and then returns
        the context data for the template, containing just a 'team_list' item
        """
        # The season_slug keyword arg should always be supplied to this view
        season_slug = kwargs['season_slug']
        season = Season.objects.get(slug=season_slug)
        update_clubstats_for_season(season)

        return {'team_list': self.get_southerners_list(season)}
