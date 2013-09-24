import logging
from django.views.generic import DetailView, ListView
from django.views.generic.edit import UpdateView
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import views as auth_views
from django.contrib.sites.models import Site
from django.conf import settings
from templated_emails.utils import send_templated_email
from braces.views import LoginRequiredMixin
from core.views import AjaxGeneral
from core.models import first_or_none
from matches.models import Appearance
from awards.models import MatchAwardWinner
from .models import Member, SquadMembership
from .forms import ProfileEditForm
from .util import get_recent_match_awards, get_recent_end_of_season_awards, get_recent_match_reports
from .stats import MemberSeasonStat
from .filters import MemberFilter

log = logging.getLogger(__name__)


def login(request, *args, **kwargs):
    if request.method == 'POST':
        if not request.POST.get('remember_me', None):
            request.session.set_expiry(0)
    return auth_views.login(request, *args, **kwargs)


class ProfileView(LoginRequiredMixin, UpdateView):
    model = Member
    template_name='registration/profile.html'
    form_class = ProfileEditForm
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        try:
            return Member.objects.get(user=self.request.user)
        except Member.DoesNotExist:
            return None

    def get_context_data(self, **kwargs):
        context = super(ProfileView, self).get_context_data(**kwargs)
        context['is_profile'] = True # Differentiates between this view and MemberDetailView
        try:
            context['member'] = Member.objects.get(user=self.request.user)
        except Member.DoesNotExist:
            context['member'] =None
        return context

    def form_valid(self, form):
        log.debug(form.cleaned_data['profile_pic'])
        log.debug(form.cleaned_data['pref_position'])
        messages.success(self.request, "Nice! Your profile has been updated.")
        return super(ProfileView, self).form_valid(form)

    def form_invalid(self, form):
        log.debug("{}".format(form.cleaned_data))

        # HACK: Make use of the invalid form for handling the 'Connect my account to a player' request
        if self.request.POST.get('request_link') == '1':
            try:
                send_templated_email([settings.SERVER_EMAIL], 'emails/req_player_link', {'user': self.request.user, 'base_url': "http://" + Site.objects.all()[0].domain })
            except:
                log.error("Failed to send player link request email for {}".format(self.request.user), exc_info=True)
                messages.error(self.request, "Sorry - we were unable to handle your request. Please try again later.")
            else:
                messages.success(self.request, "Thanks - your request to be linked to a player/club member has been sent to the website administrator.")
        else:
            messages.error(
                self.request,
                "Failed to update profile. Errors: {}".format(form.errors)
            )
        return super(ProfileView, self).form_invalid(form)

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
        context['squad'] = first_or_none(SquadMembership.objects.current().by_member(member))

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

        # This will be keyed on the season id, with a special 'totals' entry for the combined totals from all seasons.
        season_dict = {}

        for app in apps:
            # Add the appearance/match details to the relevant season's running total classes
            if not season_dict.has_key(app.match.season_id):
                season_dict[app.match.season_id] = MemberSeasonStat(season=app.match.season)

            season_dict[app.match.season_id].add_appearance(app)

        # Get all match awards won by this member
        awards = MatchAwardWinner.objects.by_member(member).select_related('match__season', 'match__our_team').filter(match__our_team__personal_stats=True)

        for award in awards:
            # Add the awards to the relevant season's running total
            if not season_dict.has_key(award.match.season_id):
                season_dict[award.match.season_id] = MemberSeasonStat(season=award.match.season)
            season_dict[award.match.season_id].matches.add_award(award)

        # Now create and calculate the combined totals for all seasons
        season_total = MemberSeasonStat()

        for season_id, season in season_dict.items():
            season_total.accumulate(season)

        seasons = sorted(season_dict.values(), key=lambda s: s.season.start)
        seasons.append(season_total)

        return {'member': member, 'seasons': seasons}
