import logging
from django.views.generic import DetailView, ListView, CreateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.template import loader, Context
from django.core.mail import send_mail, BadHeaderError
from django.core.urlresolvers import reverse
from braces.views import SelectRelatedMixin, StaffuserRequiredMixin
from core.models import ClubInfo
from core.views import AjaxGeneral
from matches.models import Appearance
from awards.models import MatchAwardWinner
from .models import Member, MembershipEnquiry
from .forms import MembershipEnquiryForm
from .util import get_recent_match_awards, get_recent_end_of_season_awards, get_recent_match_reports
from .stats import MemberSeasonStat

log = logging.getLogger(__name__)


class MemberListView(SelectRelatedMixin, ListView):
    """View with a list of all members"""
    model = Member
    select_related = ["user"]


class MemberDetailView(SelectRelatedMixin, DetailView):
    """View of a particular member"""
    model = Member
    select_related = ["user"]

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
    

class MembershipEnquiryListView(ListView):
    """View with a list of all membership enquiries"""
    model = MembershipEnquiry


class MembershipEnquiryDetailView(StaffuserRequiredMixin, DetailView):
    """View of a particular membership enquiry"""
    model = MembershipEnquiry


class MembershipEnquiryCreateView(FormView):
    """This is essentially the 'Join Us' form view"""
    model = MembershipEnquiry
    form_class = MembershipEnquiryForm
    template_name = "members/join_us.html"
    # TODO: Redirect to another page and give them more links to click on!
    success_url = '/members/enquiries/new/'

    def email_to_secretary(self, form):
        from_email = form.cleaned_data['email']
        t = loader.get_template('members/membershipenquiry_email.txt')
        c = Context({
            'name': "{} {}".format(form.cleaned_data['first_name'], form.cleaned_data['last_name']),
            'phone': form.cleaned_data['phone'],
            'email': from_email,
            'join_mail_list': form.cleaned_data['join_mail_list'],
            'hockey_exp': form.cleaned_data['hockey_exp'],
            'comments': form.cleaned_data['comments'],
        })
        subject = "New enquiry from {}".format(c['name'])
        
        message = t.render(c)
        try:
            recipient_email = ClubInfo.objects.get(key='SecretaryEmail').value
        except ClubInfo.DoesNotExist:
                recipient_email = 'secretary@cambridgesouthhockeyclub.co.uk'
        send_mail(subject, message, from_email, [recipient_email], fail_silently=False)

    def email_to_enquirer(self, form):
        t = loader.get_template('members/membershipenquiry_welcome_email.txt')
        c = Context({
            'first_name': form.cleaned_data['first_name'],
        })
        try:
            c['secretary_name'] = ClubInfo.objects.get(key='SecretaryName').value
            c['secretary_email'] = ClubInfo.objects.get(key='SecretaryEmail').value
        except ClubInfo.DoesNotExist:
            c['secretary_name'] = ""
            c['secretary_email'] = 'secretary@cambridgesouthhockeyclub.co.uk'
            
        from_email = c['secretary_email']
        subject = "Your enquiry with Cambridge South Hockey Club"
        
        message = t.render(c)
        recipient_email = form.cleaned_data['email']
        send_mail(subject, message, from_email, [recipient_email], fail_silently=False)

    def form_valid(self, form):
        try:
            self.email_to_secretary(form)
            self.email_to_enquirer(form)
            messages.info(self.request, "Thanks for your interest in Cambridge South. We'll be in touch shortly!")
        except BadHeaderError:
            log.warn("Failed to send email")
            messages.warning(self.request, "Sorry - we were unable to process your enquiry. Please try again later.")
        return super(MembershipEnquiryCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.info(
            self.request,
            "Submission failed. Errors: {}".format(form.errors)
        )
        return super(MembershipEnquiryCreateView, self).form_invalid(form)

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
