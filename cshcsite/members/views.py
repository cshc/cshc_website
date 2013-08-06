import logging
from django.views.generic import DetailView, ListView
from django.shortcuts import get_object_or_404
from core.views import AjaxGeneral
from matches.models import Appearance
from awards.models import MatchAwardWinner
from .models import Member
from .util import get_recent_match_awards, get_recent_end_of_season_awards, get_recent_match_reports
from .stats import MemberSeasonStat
from .filters import MemberFilter

log = logging.getLogger(__name__)


class MemberListView(ListView):
    """View with a list of all members"""
    model = Member

    def get_context_data(self, **kwargs):
        context = super(MemberListView, self).get_context_data(**kwargs)
        member_qs = Member.objects.all()
        context['filter'] = MemberFilter(self.request.GET, queryset=member_qs)
        return context


class MemberDetailView(DetailView):
    """View of a particular member"""
    model = Member

    def get_context_data(self, **kwargs):
        context = super(MemberDetailView, self).get_context_data(**kwargs)

        member = context["member"]

        # Add recent match reports written by this member
        context['recent_match_reports'] = get_recent_match_reports(member)

        # Add recent match awards won by this member
        context['recent_match_awards'] = get_recent_match_awards(member)

        # Add recent End Of Season awards won by this member
        context['recent_end_of_season_awards'] = get_recent_end_of_season_awards(member)

        return context


class MemberStatsView(AjaxGeneral):
    """An AJAX-only view for calculating and displaying statistics related to a particular member"""
    template_name = 'members/_member_stats.html'

    def get_template_context(self, **kwargs):
        """Get a member's match stats for all seasons """
        member_id = kwargs['pk']

        member = get_object_or_404(Member, pk=member_id)

        # Get all the appearances for this member
        apps = Appearance.objects.by_member(member).select_related('member__user', 'match__season', 'match__our_team').filter(match__our_team__personal_stats=True).order_by('match__date')
        log.debug("Got {} appearances for {}".format(apps.count(), member))

        # This will be keyed on the season id, with a special 'totals' entry for the combined totals from all seasons.
        season_dict = {}

        for app in apps:
            # Add the appearance/match details to the relevant season's running total classes
            if not season_dict.has_key(app.match.season_id):
                log.debug("Adding season stats for {}".format(app.match.season))
                season_dict[app.match.season_id] = MemberSeasonStat(season=app.match.season)

            log.debug("Adding appearance stats for match ID {}".format(app.match_id))
            season_dict[app.match.season_id].add_appearance(app)

        # Get all match awards won by this member
        awards = MatchAwardWinner.objects.by_member(member).select_related('match__season', 'match__our_team').filter(match__our_team__personal_stats=True)
        log.debug("Got {} match awards for {}".format(awards.count(), member))

        for award in awards:
            # Add the awards to the relevant season's running total
            if not season_dict.has_key(award.match.season_id):
                log.debug("Adding season stats for {}".format(award.match.season))
                season_dict[award.match.season_id] = MemberSeasonStat(season=award.match.season)
            log.debug("Adding awards stats for match ID {}".format(award.match_id))
            season_dict[award.match.season_id].matches.add_award(award)

        # Now create and calculate the combined totals for all seasons
        season_total = MemberSeasonStat()

        for season_id, season in season_dict.items():
            log.debug("Adding {} season stats to total".format(season.season))
            season_total.accumulate(season)

        seasons = sorted(season_dict.values(), key=lambda s: s.season.start)
        seasons.append(season_total)

        return {'member': member, 'seasons': seasons}
