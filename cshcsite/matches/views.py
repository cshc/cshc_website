""" Django Views relating to matches
"""

import collections
from datetime import datetime
from itertools import groupby
from django.views.generic import DetailView, ListView, TemplateView
from django.utils import timezone
from django.db.models import Q
from braces.views import SelectRelatedMixin, LoginRequiredMixin, PermissionRequiredMixin
from core.stats import MatchStats
from core.models import ClubInfo
from core.views import AjaxGeneral, get_season_from_kwargs, add_season_selector
from competitions.models import Season
from awards.models import MatchAward, MatchAwardWinner
from teams.models import ClubTeam
from members.models import Member
from matches.models import Match, GoalKing, Appearance
from matches.filters import MatchFilter


class MatchListView(ListView):
    """ A view of all matches - paginated, filterable, sortable"""
    model = Match

    def get_context_data(self, **kwargs):
        context = super(MatchListView, self).get_context_data(**kwargs)
        match_qs = Match.objects.select_related('our_team', 'opp_team__club', 'venue',
                                                'division__league', 'cup', 'season')
        match_qs = match_qs.prefetch_related('players')
        match_qs = match_qs.defer('report_body', 'pre_match_hype')
        match_qs = match_qs.order_by('-date', '-time')

        context['filter'] = MatchFilter(self.request.GET, queryset=match_qs)
        return context


class MatchesBySeasonView(TemplateView):
    """ Calendar view of all matches in a particular season. """

    template_name = 'matches/matches_by_season.html'

    def get_context_data(self, **kwargs):
        context = super(MatchesBySeasonView, self).get_context_data(**kwargs)
        season = get_season_from_kwargs(kwargs)

        match_qs = Match.objects.select_related('our_team', 'opp_team__club', 'venue',
                                                'division__league', 'cup', 'season')
        match_qs = match_qs.filter(season=season)
        match_qs = match_qs.defer('report_body', 'pre_match_hype')
        match_qs = match_qs.order_by('date', 'time')

        # Group matches by calendar year (e.g. Sept-Dec in one group, Jan-April in the other)
        year1 = [m for m in match_qs if m.date.year == season.start.year]
        year2 = [m for m in match_qs if m.date.year == season.end.year]

        matches_by_year = {
            season.start.year: self.group_by_month(year1),
            season.end.year: self.group_by_month(year2)
        }

        context['matches_by_year'] = matches_by_year

        add_season_selector(context, season, Season.objects.reversed())

        return context

    def group_by_month(self, matches):
        """ Utility method to group matches by calendar month. """
        field = lambda m: m.date.month
        return dict(
            [(month, list(matches_in_month)) for month, matches_in_month in groupby(matches, field)]
        )


class MatchesByDateView(TemplateView):
    """ View of all matches on a particular date."""

    template_name = 'matches/matches_by_date.html'

    def get_context_data(self, **kwargs):
        context = super(MatchesByDateView, self).get_context_data(**kwargs)
        match_date = datetime.strptime(kwargs['date'], "%d-%b-%y").date()

        # Get all matches on this date
        matches = Match.objects.by_date(match_date).select_related('our_team', 'opp_team__club',
                                                                   'venue', 'division__league',
                                                                   'cup', 'season')

        # Get all appearances on this date
        appearances = Appearance.objects.select_related('member__user')
        appearances = appearances.filter(match__date=match_date)

        # Get all the award winners on this date
        award_winners = MatchAwardWinner.objects.select_related('member__user', 'award')
        award_winners = award_winners.filter(match__date=match_date)

        # Create match stats object for each match. Index by match id.
        match_lookup = {match.pk: MatchStats(match) for match in matches}

        # Add appearances to match stats
        for app in appearances:
            match_lookup[app.match_id].add_appearance(app)

        # Add award winners to match stats
        for award_winner in award_winners:
            match_lookup[award_winner.match_id].add_award_winner(award_winner)

        # Sort match list by team position
        match_list = sorted(match_lookup.values(), key=lambda m: m.match.our_team.position)

        # Get previous and next match dates
        prev_match = Match.objects.only('date').filter(date__lt=match_date).order_by('-date', '-time').first()
        next_match = Match.objects.only('date').filter(date__gt=match_date).order_by('date', 'time').first()
        context['prev_date'] = prev_match.date if prev_match else None
        context['next_date'] = next_match.date if next_match else None

        context['match_list'] = match_list
        context['date'] = match_date
        return context


class LatestResultsView(TemplateView):
    """ View for the latest match results (max one per team)"""

    template_name = 'matches/latest_results.html'

    def get_context_data(self, **kwargs):
        context = super(LatestResultsView, self).get_context_data(**kwargs)
        LatestResultsView.add_latest_results_to_context(context)
        return context

    @staticmethod
    def add_latest_results_to_context(context):
        """ Helper method to add latest results to a context dictionary.
            context = the view context (a dictionary)
            Returns: the context dictionary, with a 'latest_results' entry
            containing a list of results

            The latest_results list contains a maximum of one result per team.
            Results are only included if the team is active and the match was
            played this season.
        """
        latest_results = []
        current_season = Season.current()
        today = timezone.now().date()
        for team in ClubTeam.objects.only('pk'):
            match_qs = Match.objects.select_related('our_team', 'opp_team__club', 'venue',
                                                    'division__league', 'cup', 'season')
            match_qs = match_qs.filter(our_team__active=True, our_team_id=team.pk,
                                       date__lte=today, season=current_season)
            match_qs = match_qs.order_by('-date', '-time')
            if match_qs.exists():
                # Have to ignore matches that are today but still in future.
                dt_now = datetime.now()
                for m in match_qs:
                    if m.datetime() < dt_now:
                        latest_results.append(m)
                        break

        context['latest_results'] = latest_results


class NextFixturesView(TemplateView):
    """ View for the next match fixtures (one per team)"""

    template_name = 'matches/next_fixtures.html'

    def get_context_data(self, **kwargs):
        context = super(NextFixturesView, self).get_context_data(**kwargs)
        NextFixturesView.add_next_fixtures_to_context(context)
        return context

    @staticmethod
    def add_next_fixtures_to_context(context):
        """ Helper method to add next fixtures to a context dictionary.
            context = the view context (a dictionary)
            Returns: the context dictionary, with a 'next_fixtures' entry
                     containing a list of fixtures

            The next_fixtures list contains a maximum of one fixture per team.
        """
        next_fixtures = []
        today = timezone.now().date()
        for team in ClubTeam.objects.only('pk'):
            match_qs = Match.objects.select_related('our_team', 'opp_team__club', 'venue',
                                                   'division__league', 'cup', 'season')
            match_qs = match_qs.filter(our_team_id=team.pk, date__gte=today)
            match_qs = match_qs.order_by('date', 'time')
            if match_qs.exists():
                # Have to ignore matches that are today but still in future.
                dt_now = datetime.now()
                for m in match_qs:
                    if m.datetime() > dt_now:
                        next_fixtures.append(m)
                        break

        context['next_fixtures'] = next_fixtures


class MatchDetailView(SelectRelatedMixin, DetailView):
    """ View providing details of a particular match"""
    model = Match
    select_related = ['our_team', 'opp_team__club', 'venue', 'division__league', 'cup', 'season']

    def get_context_data(self, **kwargs):
        """
        Gets the context data for the view.

        In addition to the 'match' item, the following are also added to the context:
            - same_date_matches:    a list of matches on the same day (not including
                                    the match being viewed)
            - mom_winners:          a list of 'Man of the Match' award winners
            - lom_winners:          a list of 'Lemon of the Match' award winners
            - appearances:          a list of appearances in this match
            - prev_match:           the previous match this team played
            - next_match:           the next match this team played/is due to play
        """
        context = super(MatchDetailView, self).get_context_data(**kwargs)
        match = context["match"]

        # Add various bits of info to the context object
        same_date_matches = Match.objects.filter(date=match.date).exclude(pk=match.pk)

        award_winners = match.award_winners.select_related('award', 'member__user').all()

        appearances = match.appearances.select_related('member__user').all()
        appearances = appearances.order_by('member__pref_position')

        match_qs = Match.objects.select_related('our_team', 'opp_team__club').filter(our_team=match.our_team)

        prev_match = match_qs.filter(date__lt=match.date).order_by('-date', '-time').first()

        next_match = match_qs.filter(date__gt=match.date).first()

        context["same_date_matches"] = same_date_matches
        context["mom_winners"] = [x for x in award_winners if x.award.name == MatchAward.MOM]
        context["lom_winners"] = [x for x in award_winners if x.award.name == MatchAward.LOM]
        context["appearances"] = appearances
        context["prev_match"] = prev_match
        context["next_match"] = next_match

        live_comments_enabled, _ = ClubInfo.objects.get_or_create(key='EnableLiveComments', defaults={'value': 'False'})

        context["enable_live_comments"] = live_comments_enabled.value in ['True', 'true', 'yes', '1']
        return context


class GoalKingMixin(object):
    """ Provides useful methods for GoalKing related views"""

    def get_goalking_list(self, season):
        """ Returns a list of GoalKing items for the specified season"""
        goalking_qs = GoalKing.objects.by_season(season).select_related('member__user')
        # We convert the queryset to a list so we can add a 'rank' attribute to each item
        goalking_list = [x for x in goalking_qs if x.total_goals > 0]

        # Apply ranking
        if len(goalking_list) > 0:
            m_list = [x for x in goalking_list if x.member.gender == Member.GENDER.Male]
            l_list = [x for x in goalking_list if x.member.gender == Member.GENDER.Female]
            self.apply_ranking(m_list)
            self.apply_ranking(l_list)

        return goalking_list

    def apply_ranking(self, goalking_list):
        """ Adds a rank attribute to each GoalKing instance in the given list
            based on the total number of goals scored by that person.
        """
        if len(goalking_list) == 0:
            return
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
    """ View for displaying the Goal King stats for a particular season. """

    template_name = 'matches/goalking.html'

    def get_context_data(self, **kwargs):
        """ Gets the context data for the view.

            In addition to the 'goalking_list' item, the following are also
            added to the context:
            - season:               the season these stats applies to
            - season_list:          a list of all seasons
        """
        context = super(GoalKingSeasonView, self).get_context_data(**kwargs)
        season = get_season_from_kwargs(kwargs)

        context['goalking_list'] = self.get_goalking_list(season)

        add_season_selector(context, season, Season.objects.reversed())

        return context


class GoalKingSeasonUpdateView(GoalKingMixin, AjaxGeneral):
    """ View for updating and then displaying Goal King stats for a particular season. """

    template_name = 'matches/_goalking_table.html'

    def get_template_context(self, **kwargs):
        """ Updates the GoalKing stats for the specified season and then returns
            the context data for the template, containing just a 'goalking_list' item
        """
        # The season_slug keyword arg should always be supplied to this view
        season = Season.objects.get(slug=kwargs['season_slug'])
        GoalKing.update_for_season(season)

        return {'goalking_list': self.get_goalking_list(season)}


class AccidentalTouristMixin(object):
    """ Provides useful methods for AccidentalTourist related views. """

    def get_goalking_list(self, season):
        """ Returns a list of GoalKing items for the specified season. """

        # We convert the queryset to a list so we can add a 'rank' attribute to each item
        goalking_list = list(GoalKing.objects.accidental_tourist(season))

        # Apply ranking
        if len(goalking_list) > 0:
            m_list = [x for x in goalking_list if x.member.gender == Member.GENDER.Male]
            l_list = [x for x in goalking_list if x.member.gender == Member.GENDER.Female]
            self.apply_ranking(m_list)
            self.apply_ranking(l_list)

        return goalking_list


    def apply_ranking(self, goalking_list):
        """ Adds a rank attribute to each GoalKing instance in the given list.
            based on the total number of miles travelled by that person.
        """
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
        """ Gets the context data for the view.

            In addition to the 'goalking_list' item, the following are also added to the context:
            - season:               the season these stats applies to
            - season_list:          a list of all seasons
        """
        context = super(AccidentalTouristSeasonView, self).get_context_data(**kwargs)
        season = get_season_from_kwargs(kwargs)

        context['goalking_list'] = self.get_goalking_list(season)

        add_season_selector(context, season, Season.objects.reversed())

        return context


class AccidentalTouristSeasonUpdateView(AccidentalTouristMixin, AjaxGeneral):
    """ View for updating and then displaying Accidental Tourist stats for a
        particular season
    """
    template_name = 'matches/_accidental_tourist_table.html'

    def get_template_context(self, **kwargs):
        """ Updates the AccidentalTourist stats for the specified season and then returns
            the context data for the template, containing just a 'goalking_list' item
        """
        # The season_slug keyword arg should always be supplied to this view
        season = Season.objects.get(slug=kwargs['season_slug'])
        GoalKing.update_for_season(season)

        return {'goalking_list': self.get_goalking_list(season)}


class NaughtyStepView(TemplateView):
    """ Table of all players who have received cards, ordered by:
        i) most red cards
        ii) most yellow cards
        iii) most green cards
    """

    template_name = 'matches/naughty_step.html'

    def get_context_data(self, **kwargs):
        context = super(NaughtyStepView, self).get_context_data(**kwargs)

        query = Q(red_card=True) | Q(yellow_card=True) | Q(green_card=True)
        card_apps = Appearance.objects.filter(query).order_by('match__date')

        players = {}
        for app in card_apps:
            if app.member not in players:
                players[app.member] = NaughtyPlayer(app.member)
            players[app.member].add_appearance(app)

        # Cumulative sort in ascending order of priority
        # (first by green, then by yellow then by red)
        players = sorted(players.values(), key=lambda p: len(p.green_cards), reverse=True)
        players = sorted(players, key=lambda p: len(p.yellow_cards), reverse=True)
        players = sorted(players, key=lambda p: len(p.red_cards), reverse=True)
        context['players'] = players
        return context


class NaughtyPlayer(object):
    """ Encapsulates a member who has received at least one card. """

    def __init__(self, member):
        self.member = member
        self.red_cards = []
        self.yellow_cards = []
        self.green_cards = []

    def add_appearance(self, appearance):
        """ Adds the cards from an appearance to the running totals for this member."""
        if appearance.member != self.member:
            raise AssertionError("This appearance, {}, does not relate to {}.".format(appearance, self.member))
        if appearance.red_card:
            self.red_cards.append(appearance)
        elif appearance.yellow_card:
            self.yellow_cards.append(appearance)
        elif appearance.green_card:
            self.green_cards.append(appearance)


class AppearancesByDateView(LoginRequiredMixin, PermissionRequiredMixin, TemplateView):
    template_name = 'matches/appearances_by_date.html'
    permission_required = "matches.add_appearance"

    def get_context_data(self, **kwargs):
        context = super(AppearancesByDateView, self).get_context_data(**kwargs)
        date = datetime.strptime(kwargs['date'], "%d-%b-%y").date()
        apps = Appearance.objects.select_related('match', 'member').filter(match__date=date).order_by('match__our_team__position', 'member__last_name')
        
        genders = collections.OrderedDict()
        
        for app in apps:
            gender = app.match.our_team.get_gender_display()
            team_name = app.match.our_team.long_name
            if gender not in genders:
                genders[gender] = {
                    'teams': collections.OrderedDict(),
                    'total': 0,
                    'double_ups': 0,
                }
            gender_struct = genders[gender]
            if team_name not in gender_struct['teams']:
                gender_struct['teams'][team_name] = {
                    'appearances': [],
                    'double_ups': 0,
                    'match': app.match,
                }
            team = gender_struct['teams'][team_name]

            has_double_up = False

            # Try to find this member in the struct already (check for double-ups)
            for t, t_struct in gender_struct['teams'].iteritems():
                double_up = next((x for x in t_struct['appearances'] if x['appearance'].member_id is app.member_id), None)
                if double_up is not None:
                    t_struct['double_ups'] += 1
                    gender_struct['double_ups'] += 1
                    has_double_up = True

            team['appearances'].append({'appearance': app, 'double_up': has_double_up})
            gender_struct['total'] += 1

        # Get previous and next match dates
        prev_match = Match.objects.only('date').filter(date__lt=date).order_by('-date', '-time').first()
        next_match = Match.objects.only('date').filter(date__gt=date).order_by('date', 'time').first()
        context['prev_date'] = prev_match.date if prev_match else None
        context['next_date'] = next_match.date if next_match else None
        
        context['appearances'] = genders
        context['date'] = date
        return context