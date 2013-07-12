import logging
from datetime import datetime, date
from django.views.generic import DetailView, ListView, TemplateView
from exceptions import IndexError
from braces.views import SelectRelatedMixin
from core.models import first_or_none
from core.stats import MatchStats
from core.views import kwargs_or_none, AjaxGeneral
from competitions.models import Season
from awards.models import MatchAward, MatchAwardWinner
from teams.models import ClubTeam
from .models import Match, GoalKing, Appearance
from .filters import MatchFilter

log = logging.getLogger(__name__)


class MatchListView(ListView):
    """A generic match list view"""
    model = Match

    def get_context_data(self, **kwargs):
        context = super(MatchList, self).get_context_data(**kwargs)
        match_qs = Match.objects.select_related('our_team', 'opp_team__club', 'venue', 'division__league', 'cup', 'season')
        context['filter'] = MatchFilter(self.request.GET, queryset=match_qs)
        return context


class MatchesByDateView(TemplateView):

    template_name='matches/matches_by_date.html'

    def get_context_data(self, **kwargs):
        context = super(MatchesByDateView, self).get_context_data(**kwargs)
                
        date_str = kwargs['date']
        dt = datetime.strptime(date_str, "%d-%b-%y")

        # Get all matches on this date
        matches = Match.objects.by_date(dt.date()).select_related('our_team', 'opp_team__club', 'venue', 'division__league', 'cup', 'season')

        # Get all appearances on this date
        appearances = Appearance.objects.select_related('member__user').filter(match__date=dt.date())

        # Get all the award winners on this date
        award_winners = MatchAwardWinner.objects.select_related('member__user', 'award').filter(match__date=dt.date())

        match_lookup = { match.pk: MatchStats(match) for match in matches}

        for app in appearances:
            match_lookup[app.match_id].add_appearance(app)

        for award_winner in award_winners:
            match_lookup[award_winner.match_id].add_award_winner(award_winner)

        match_list = sorted(match_lookup.values(), key=lambda m: m.match.our_team.position)

        # Get previous and next dates
        prev_match = first_or_none(Match.objects.only('date').filter(date__lt=dt.date()).order_by('-date'))
        next_match = first_or_none(Match.objects.only('date').filter(date__gt=dt.date()).order_by('date'))
        context['prev_date'] = prev_match.date if prev_match else None
        context['next_date'] = next_match.date if next_match else None
        
        context['match_list'] = match_list
        context['date'] = dt.date()
        return context

class LatestResultsView(TemplateView):
    """View for the latest results (one per team)"""

    template_name='matches/latest_results.html'

    def get_context_data(self, **kwargs):
        context = super(LatestResultsView, self).get_context_data(**kwargs)
        LatestResultsView.add_latest_results_to_context(context)
        return context

    @staticmethod
    def add_latest_results_to_context(context):
        """
        Helper method to add latest results to a context dictionary.
        context = the view context (a dictionary)
        Returns: the context dictionary, with a 'latest_results' entry containing a list of results

        The latest_results list contains a maximum of one result per team.
        """
        latest_results = []
        for team in ClubTeam.objects.only('pk'):
            try:
                result = Match.objects.select_related('our_team', 'opp_team__club', 'venue', 'division__league', 'cup', 'season').filter(our_team_id=team.pk, date__lt=datetime.now().date()).order_by('-date')[0]
                latest_results.append(result)
            except IndexError:
                pass    # Don't worry if there's no latest result for that team

        context['latest_results'] = latest_results


class NextFixturesView(TemplateView):
    """View for the next match fixtures (one per team)"""

    template_name = 'matches/next_fixtures.html'

    def get_context_data(self, **kwargs):
        context = super(NextFixturesView, self).get_context_data(**kwargs)
        NextFixturesView.add_next_fixtures_to_context(context)
        return context

    @staticmethod
    def add_next_fixtures_to_context(context):
        """
        Helper method to add next fixtures to a context dictionary.
        context = the view context (a dictionary)
        Returns: the context dictionary, with a 'next_fixtures' entry containing a list of fixtures

        The next_fixtures list contains a maximum of one fixture per team.
        """
        next_fixtures = []
        for team in ClubTeam.objects.only('pk'):
            try:
                fixture = Match.objects.select_related('our_team', 'opp_team__club', 'venue', 'division__league', 'cup', 'season').filter(our_team_id=team.pk).fixtures()[0]
                next_fixtures.append(fixture)
            except IndexError:
                pass    # Don't worry if there's no next fixture for that team

        context['next_fixtures'] = next_fixtures


class MatchDetailView(SelectRelatedMixin, DetailView):
    """View providing details of a particular match"""
    model = Match
    select_related = ['our_team', 'opp_team__club', 'venue', 'division__league', 'cup', 'season']

    def get_context_data(self, **kwargs):
        """
        Gets the context data for the view.

        In addition to the 'match' item, the following are also added to the context:
            - same_date_matches:    a list of matches on the same day (not including the match being viewed)
            - award_winners:        a list of match award winners
            - appearances:          a list of appearances in this match
            - prev_match:           the previous match this team played
            - next_match:           the next match this team played/is due to play
        """
        context = super(MatchDetailView, self).get_context_data(**kwargs)
    
        match = context["match"]
        # Add various bits of info to the context object
        same_date_matches = Match.objects.filter(date=match.date).exclude(pk=match.pk)
        award_winners = match.award_winners.select_related('award', 'member__user').all()
        appearances = match.appearances.select_related('member__user').all().order_by('member__pref_position')
        prev_match = first_or_none(Match.objects.select_related('our_team', 'opp_team__club').order_by('-date').filter(our_team=match.our_team, date__lt=match.date))
        next_match = first_or_none(Match.objects.select_related('our_team', 'opp_team__club').filter(our_team=match.our_team, date__gt=match.date))

        context["same_date_matches"] = same_date_matches
        context["mom_winners"] = filter(lambda x: x.award.name == MatchAward.MOM, award_winners)
        context["lom_winners"] = filter(lambda x: x.award.name == MatchAward.LOM, award_winners)
        context["appearances"] = appearances
        context["prev_match"] = prev_match
        context["next_match"] = next_match

        return context


class GoalKingMixin(object):
    """Provides useful methods for GoalKing related views"""

    def get_goalking_list(self, season):
        """Returns a list of GoalKing items for the specified season"""

        # We convert the queryset to a list so we can add a 'rank' attribute to each item 
        goalking_list = list(GoalKing.objects.by_season(season).select_related('member__user'))

        # Apply ranking
        if len(goalking_list) > 0:
            rank = 1
            previous = goalking_list[0]
            previous.rank = 1
            for i, entry in enumerate(goalking_list[1:]):
                if entry.total_goals != previous.total_goals:
                    rank = i + 2
                    entry.rank = str(rank)
                else:
                    entry.rank = "%s=" % rank
                    previous.rank = entry.rank
                previous = entry

        return goalking_list


class GoalKingSeasonView(GoalKingMixin, TemplateView):
    """View for displaying the Goal King stats for a particular season"""
    template_name = 'matches/goalking.html'
    
    def get_context_data(self, **kwargs):
        """
        Gets the context data for the view.

        In addition to the 'goalking_list' item, the following are also added to the context:
            - season:               the season these stats applies to
            - season_list:          a list of all seasons
        """
        context = super(GoalKingSeasonView, self).get_context_data(**kwargs)

        # If we're viewing this season's stats we may not have a season_slug keyword arg.
        season_slug = kwargs_or_none('season_slug', **kwargs)
        if season_slug != None:
            season = Season.objects.get(slug=season_slug)
        else:
            season = Season.current()

        context['goalking_list'] = self.get_goalking_list(season)

        context['season'] = season
        context['season_list'] = Season.objects.all()
        return context


class GoalKingSeasonUpdateView(GoalKingMixin, AjaxGeneral):
    """View for updating and then displaying Goal King stats for a particular season"""
    template_name = 'matches/_goalking_table.html'

    def get_template_context(self, **kwargs):
        """
        Updates the GoalKing stats for the specified season and then returns
        the context data for the template, containing just a 'goalking_list' item
        """
        # The season_slug keyword arg should always be supplied to this view
        season_slug = kwargs['season_slug']
        season = Season.objects.get(slug=season_slug)
        GoalKing.update_for_season(season)

        return { 'goalking_list': self.get_goalking_list(season) }

