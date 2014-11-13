import logging
import operator
from datetime import datetime, date, timedelta
from itertools import groupby
from django.views.generic import DetailView, ListView, TemplateView
from django.utils import timezone
from django.db.models import Q
from django.db import IntegrityError
from exceptions import IndexError
from braces.views import SelectRelatedMixin
from core.models import first_or_none
from core.stats import MatchStats
from core.views import kwargs_or_none, AjaxGeneral
from competitions.models import Season
from awards.models import MatchAward, MatchAwardWinner
from teams.models import ClubTeam
from members.models import Member
from .models import Match, GoalKing, Appearance
from .filters import MatchFilter

log = logging.getLogger(__name__)


class MatchListView(ListView):
    """A generic match list view"""
    model = Match

    def get_context_data(self, **kwargs):
        context = super(MatchListView, self).get_context_data(**kwargs)
        match_qs = Match.objects.select_related('our_team', 'opp_team__club', 'venue', 'division__league', 'cup', 'season')
        match_qs = match_qs.prefetch_related('players').defer('report_body', 'pre_match_hype').order_by('-date', '-time')
        context['filter'] = MatchFilter(self.request.GET, queryset=match_qs)
        return context


class MatchesBySeasonView(TemplateView):

    template_name = 'matches/matches_by_season.html'
    season_slug = None

    def get_context_data(self, **kwargs):
        context = super(MatchesBySeasonView, self).get_context_data(**kwargs)

        season_slug = kwargs_or_none('season_slug', **kwargs)
        if season_slug is not None:
            season = Season.objects.get(slug=season_slug)
        else:
            season = Season.current()

        match_list = Match.objects.select_related('our_team', 'opp_team__club', 'venue', 'division__league', 'cup', 'season').filter(season=season).defer('report_body', 'pre_match_hype').order_by('date', 'time')

        m1 = filter(lambda m: m.date.year == season.start.year, match_list)
        m2 = filter(lambda m: m.date.year == season.end.year, match_list)

        matches_by_year = {season.start.year: self.group_by_month(m1), season.end.year: self.group_by_month(m2)}

        context['matches_by_year'] = matches_by_year
        context['season'] = season
        context['season_list'] = Season.objects.all().order_by("-start")

        return context

    def group_by_month(self, matches):
        field = lambda m: m.date.month
        return dict(
            [(month, list(matches_in_month)) for month, matches_in_month in groupby(matches, field)]
        )


class MatchesByDateView(TemplateView):

    template_name = 'matches/matches_by_date.html'

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

        match_lookup = {match.pk: MatchStats(match) for match in matches}

        for app in appearances:
            match_lookup[app.match_id].add_appearance(app)

        for award_winner in award_winners:
            match_lookup[award_winner.match_id].add_award_winner(award_winner)

        match_list = sorted(match_lookup.values(), key=lambda m: m.match.our_team.position)

        # Get previous and next dates
        prev_match = first_or_none(Match.objects.only('date').filter(date__lt=dt.date()).order_by('-date', '-time'))
        next_match = first_or_none(Match.objects.only('date').filter(date__gt=dt.date()).order_by('date', 'time'))
        context['prev_date'] = prev_match.date if prev_match else None
        context['next_date'] = next_match.date if next_match else None

        context['match_list'] = match_list
        context['date'] = dt.date()
        return context


class LatestResultsView(TemplateView):
    """View for the latest results (one per team)"""

    template_name = 'matches/latest_results.html'

    def get_context_data(self, **kwargs):
        context = super(LatestResultsView, self).get_context_data(**kwargs)
        LatestResultsView.add_latest_results_to_context(context, self.request.user)
        return context

    @staticmethod
    def add_latest_results_to_context(context, user):
        """
        Helper method to add latest results to a context dictionary.
        context = the view context (a dictionary)
        user = the request user (may be anonymous if not logged in)
        Returns: the context dictionary, with a 'latest_results' entry containing a list of results

        The latest_results list contains a maximum of one result per team.
        """
        latest_results = []
        for team in ClubTeam.objects.only('pk'):
            try:
                now = timezone.now()
                min_date = now - timedelta(days=365)
                result = Match.objects.select_related('our_team', 'opp_team__club', 'venue', 'division__league', 'cup', 'season').filter(our_team_id=team.pk, date__gt=min_date.date(), date__lt=now.date()).order_by('-date', '-time')[0]
                latest_results.append(result)
            except IndexError:
                pass    # Don't worry if there's no latest result for that team

        context['latest_results'] = latest_results

        if hasattr(user, 'member') and user.member is not None:
            my_latest_result = Appearance.latest_match(user.member)
            if my_latest_result is not None:
                for result in latest_results:
                    result.is_mine = result.id == my_latest_result.match.id
            context['my_latest_result'] = my_latest_result


class NextFixturesView(TemplateView):
    """View for the next match fixtures (one per team)"""

    template_name = 'matches/next_fixtures.html'

    def get_context_data(self, **kwargs):
        context = super(NextFixturesView, self).get_context_data(**kwargs)
        NextFixturesView.add_next_fixtures_to_context(context, self.request.user)
        return context

    @staticmethod
    def add_next_fixtures_to_context(context, user):
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

        if hasattr(user, 'member') and user.member is not None:
            my_next_fixture = Appearance.probable_next_match(user.member)
            if my_next_fixture is not None:
                for fixture in next_fixtures:
                    fixture.is_mine = fixture.id == my_next_fixture.match.id
            context['my_next_fixture'] = my_next_fixture


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
        prev_match = first_or_none(Match.objects.select_related('our_team', 'opp_team__club').order_by('-date', '-time').filter(our_team=match.our_team, date__lt=match.date))
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
        goalking_list = filter(lambda x: x.total_goals > 0, GoalKing.objects.by_season(season).select_related('member__user'))

        # Apply ranking

        if len(goalking_list) > 0:
            m_list = filter(lambda x: x.member.gender == Member.GENDER.Male, goalking_list)
            l_list = filter(lambda x: x.member.gender == Member.GENDER.Female, goalking_list)
            self.apply_ranking(m_list)
            self.apply_ranking(l_list)

        return goalking_list

    def apply_ranking(self, goalking_list):
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
        if season_slug is not None:
            season = Season.objects.get(slug=season_slug)
        else:
            season = Season.current()

        context['goalking_list'] = self.get_goalking_list(season)

        context['season'] = season
        context['season_list'] = Season.objects.all().order_by("-start")
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

        return {'goalking_list': self.get_goalking_list(season)}


class AccidentalTouristMixin(object):
    """Provides useful methods for AccidentalTourist related views"""

    def get_goalking_list(self, season):
        """Returns a list of GoalKing items for the specified season"""

        # We convert the queryset to a list so we can add a 'rank' attribute to each item
        goalking_list = list(GoalKing.objects.accidental_tourist(season))

        # Apply ranking
        m_list = filter(lambda x: x.member.gender == Member.GENDER.Male, goalking_list)
        l_list = filter(lambda x: x.member.gender == Member.GENDER.Female, goalking_list)
        self.apply_ranking(m_list)
        self.apply_ranking(l_list)

        return goalking_list


    def apply_ranking(self, goalking_list):
        if len(goalking_list) == 0:
            return
        rank = 1
        previous = goalking_list[0]
        previous.rank = 1
        for i, entry in enumerate(goalking_list[1:]):
            if entry.total_miles != previous.total_miles:
                rank = i + 2
                entry.rank = str(rank)
            else:
                entry.rank = "%s=" % rank
                previous.rank = entry.rank
            previous = entry


class AccidentalTouristSeasonView(AccidentalTouristMixin, TemplateView):
    """ View for displaying the Accidental Tourist (total miles travelled)
        stats for a particular season
    """
    template_name = 'matches/accidental_tourist.html'

    def get_context_data(self, **kwargs):
        """
        Gets the context data for the view.

        In addition to the 'goalking_list' item, the following are also added to the context:
            - season:               the season these stats applies to
            - season_list:          a list of all seasons
        """
        context = super(AccidentalTouristSeasonView, self).get_context_data(**kwargs)

        # If we're viewing this season's stats we may not have a season_slug keyword arg.
        season_slug = kwargs_or_none('season_slug', **kwargs)
        if season_slug is not None:
            season = Season.objects.get(slug=season_slug)
        else:
            season = Season.current()

        context['goalking_list'] = self.get_goalking_list(season)

        context['season'] = season
        context['season_list'] = Season.objects.all().order_by("-start")
        return context


class AccidentalTouristSeasonUpdateView(AccidentalTouristMixin, AjaxGeneral):
    """ View for updating and then displaying Accidental Tourist stats for a
        particular season
    """
    template_name = 'matches/_accidental_tourist_table.html'

    def get_template_context(self, **kwargs):
        """
        Updates the AccidentalTourist stats for the specified season and then returns
        the context data for the template, containing just a 'goalking_list' item
        """
        # The season_slug keyword arg should always be supplied to this view
        season_slug = kwargs['season_slug']
        season = Season.objects.get(slug=season_slug)
        GoalKing.update_for_season(season)

        return {'goalking_list': self.get_goalking_list(season)}




class NaughtyStepView(TemplateView):

    template_name = 'matches/naughty_step.html'

    def get_context_data(self, **kwargs):
        context = super(NaughtyStepView, self).get_context_data(**kwargs)

        q = Q(red_card=True) | Q(yellow_card=True) | Q(green_card=True)
        card_apps = Appearance.objects.filter(q).order_by('match__date')

        players = {}
        for app in card_apps:
            if app.member not in players:
                players[app.member] = NaughtyPlayer(app.member)
            players[app.member].add_appearance(app)

        players = sorted(players.values(), key=lambda p: len(p.green_cards), reverse=True)
        players = sorted(players, key=lambda p: len(p.yellow_cards), reverse=True)
        players = sorted(players, key=lambda p: len(p.red_cards), reverse=True)
        context['players'] = players
        return context


class NaughtyPlayer(object):

    def __init__(self, member):
        self.member = member
        self.red_cards = []
        self.yellow_cards = []
        self.green_cards = []

    def add_appearance(self, appearance):
        if appearance.member != self.member:
            raise IntegrityError("This appearance, {}, does not relate to {}.".format(appearance, self.member))
        if appearance.red_card:
            self.red_cards.append(appearance)
        elif appearance.yellow_card:
            self.yellow_cards.append(appearance)
        elif appearance.green_card:
            self.green_cards.append(appearance)