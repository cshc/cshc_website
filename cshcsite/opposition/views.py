import logging
from collections import defaultdict
from django.views.generic import DetailView, ListView, TemplateView
from braces.views import SelectRelatedMixin, PrefetchRelatedMixin
from core.views import AjaxGeneral
from matches.models import Match, Appearance
from awards.models import MatchAwardWinner
from core.stats import MatchStats
from . import stats
from .models import Club, Team, ClubStats

log = logging.getLogger(__name__)


class ClubListView(TemplateView):
    """View for a list of opposition clubs"""

    template_name = 'opposition/club_list.html'
    model = Club

    def get_context_data(self, **kwargs):
        context = super(ClubListView, self).get_context_data(**kwargs)

        club_stats = ClubStats.objects.totals()
        context['clubstats_list'] = club_stats
        return context


class ClubStatsUpdateView(AjaxGeneral):
    """View for updating and then displaying Opposition Club stats"""
    template_name = 'opposition/_clubstats_table.html'

    def get_template_context(self, **kwargs):
        """
        Updates the Opposition Club stats and then returns the context data
        for the template, containing just a 'clubstats_list' item
        """

        return { 'clubstats_list': stats.update_all_club_stats() }

class ClubDetailView(TemplateView):
    """View for a particular opposition club"""

    template_name = 'opposition/club_detail.html'
    model = Club

    def get_context_data(self, **kwargs):
        context = super(ClubDetailView, self).get_context_data(**kwargs)
        club_slug = kwargs['slug']
        club = Club.objects.get(slug=club_slug)
        club_stats = list(ClubStats.objects.select_related('club', 'team').order_by('team__position').filter(club=club))

        # Get all matches against this club
        matches = Match.objects.select_related('our_team', 'opp_team__club', 'venue', 'division__league', 'cup', 'season').filter(opp_team__club=club).order_by('date')

        # Get all appearances against this club
        appearances = Appearance.objects.select_related('member__user').filter(match__opp_team__club=club)

        # Get all the award winners against this club
        award_winners = MatchAwardWinner.objects.select_related('member__user', 'award').filter(match__opp_team__club=club)

        match_lookup = { match.pk: MatchStats(match) for match in matches}

        for app in appearances:
            match_lookup[app.match_id].add_appearance(app)

        for award_winner in award_winners:
            match_lookup[award_winner.match_id].add_award_winner(award_winner)


        all_team_fixtures = {}
        [all_team_fixtures.setdefault(ms.match.our_team, []).append(ms) for _, ms in match_lookup.iteritems()]
        for team, fixtures in all_team_fixtures.iteritems():
            all_team_fixtures[team] = sorted(fixtures, key=lambda f: f.match.date)

        # Shift the totals column to the end of the list
        if club_stats:
            all_teams = filter(lambda c: c.team is None, club_stats)[0]
            assert all_teams.team is None
            club_stats.remove(all_teams)
            club_stats.append(all_teams)

        context['club'] = club
        context['clubstats_list'] = club_stats
        context['all_team_fixtures'] = all_team_fixtures
        return context

# Not implemented

# class TeamListView(SelectRelatedMixin, ListView):
#     """View for a list of opposition teams"""

#     model = Team
#     select_related = ["club"]


# class TeamDetailView(SelectRelatedMixin, DetailView):
#     """View for a particular opposition team"""

#     model = Team
#     select_related = ["club"]