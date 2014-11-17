import logging
from django.views.generic import TemplateView
from django.conf import settings
from core.views import kwargs_or_none
from core.models import ClubInfo, TeamGender
from competitions.models import Season
from matches.views import LatestResultsView, NextFixturesView
from training.views import UpcomingTrainingSessionsView
from members.models import CommitteeMembership
from venues.models import Venue

log = logging.getLogger(__name__)


class HomeView(TemplateView):
    """The main home page of the Cambridge South Hockey Club website"""
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        # Latest Results
        LatestResultsView.add_latest_results_to_context(context, self.request.user)

        # Next Fixtures
        NextFixturesView.add_next_fixtures_to_context(context, self.request.user)

        # Upcoming Training
        UpcomingTrainingSessionsView.add_upcoming_training_to_context(context)

        # The top banner style can be modified by the value of the 'HomePageBanner'
        # ClubInfo database item. Currently the supported values are:
        #    - 'default': displays latest results and next fixtures
        #    - 'summer': displays an advert for Summer Hockey
        try:
            banner_style = ClubInfo.objects.get(key='HomePageBanner').value
        except ClubInfo.DoesNotExist:
            banner_style = "default"

        context['banner_style'] = banner_style

        return context


class AboutUsView(TemplateView):
    """Background and History"""
    template_name = 'core/about_us.html'

    def get_context_data(self, **kwargs):
        context = super(AboutUsView, self).get_context_data(**kwargs)

        return context


class CalendarView(TemplateView):
    template_name='core/calendar.html'

    def get_context_data(self, **kwargs):
        # Tip: Login to google calendar cshc.club@gmail.com (password in 'Account Details' Google Doc) to get these addresses
        context = super(CalendarView, self).get_context_data(**kwargs)
        context['l1_gcal'] = '3r9qabjcbhh6jmfksbd3rdhldq41ss2s@import.calendar.google.com'
        context['l2_gcal'] = '2vkrhsi8la89bbc88gbvka8o0phmgdq1@import.calendar.google.com'
        context['l3_gcal'] = 'ls152bvh17a4h3t6920qbdg9flr2fhuo@import.calendar.google.com'
        context['m1_gcal'] = 'qf04nd137chqcb4sfj14iv9rqeeo8r12@import.calendar.google.com'
        context['m2_gcal'] = '8bfneiki1pl0v2dgm7dok7oeai5p545n@import.calendar.google.com'
        context['m3_gcal'] = '5ldru6voa2bfli0dt7q1afmopdts1e82@import.calendar.google.com'
        context['m4_gcal'] = '0mbj8h3g1tja0mau6vsr42lsuapjb2j3@import.calendar.google.com'
        context['m5_gcal'] = 'c5kcqb9nvg4249e4l2oi62f5r73cbch6@import.calendar.google.com'
        context['all_gcal'] = 'i7ngcunrs8icf3btp6llk1eav1bvuqol@import.calendar.google.com'
        context['training_gcal'] = '55b76kp09vmmck17985jt8qce08e9jee@import.calendar.google.com'
        context['events_gcal'] = 't7dhl1k54rqb6mmt0huu778ac8@group.calendar.google.com'
        return context



class CommitteeSeasonView(TemplateView):
    """View for displaying the Club Committee members for a particular season"""
    template_name = 'core/committee.html'

    def get_context_data(self, **kwargs):
        """
        Gets the context data for the view.

        """
        context = super(CommitteeSeasonView, self).get_context_data(**kwargs)

        # If we're viewing this season's committee we may not have a season_slug keyword arg.
        season_slug = kwargs_or_none('season_slug', **kwargs)
        if season_slug is not None:
            season = Season.objects.get(slug=season_slug)
        else:
            season = Season.current()

        all_members = CommitteeMembership.objects.select_related('position', 'member', 'season').by_season(season)

        context['general_committee'] = [m for m in all_members if m.position.gender == TeamGender.Mixed]
        ladies_committee = [m for m in all_members if m.position.gender == TeamGender.Ladies]
        mens_committee = [m for m in all_members if m.position.gender == TeamGender.Mens]

        context['ladies_captains'] = [{
            'name': "Ladies 1st team",
            'captain': next((m for m in ladies_committee if m.position.name == "Ladies' 1st XI Captain"), None),
            'vice_captain': next((m for m in ladies_committee if m.position.name == "Ladies' 1st XI Vice-Captain"), None)
        },{
            'name': "Ladies 2nd team",
            'captain': next((m for m in ladies_committee if m.position.name == "Ladies' 2nd XI Captain"), None),
            'vice_captain': next((m for m in ladies_committee if m.position.name == "Ladies' 2nd XI Vice-Captain"), None)
        },{
            'name': "Ladies 3rd team",
            'captain': next((m for m in ladies_committee if m.position.name == "Ladies' 3rd XI Captain"), None),
            'vice_captain': next((m for m in ladies_committee if m.position.name == "Ladies' 3rd XI Vice-Captain"), None)
        }]


        context['mens_captains'] = [{
            'name': "Mens 1st team",
            'captain': next((m for m in mens_committee if m.position.name == "Men's 1st XI Captain"), None),
            'vice_captain': next((m for m in mens_committee if m.position.name == "Men's 1st XI Vice-Captain"), None)
        },{
            'name': "Mens 2nd team",
            'captain': next((m for m in mens_committee if m.position.name == "Men's 2nd XI Captain"), None),
            'vice_captain': next((m for m in mens_committee if m.position.name == "Men's 2nd XI Vice-Captain"), None)
        },{
            'name': "Mens 3rd team",
            'captain': next((m for m in mens_committee if m.position.name == "Men's 3rd XI Captain"), None),
            'vice_captain': next((m for m in mens_committee if m.position.name == "Men's 3rd XI Vice-Captain"), None)
        },{
            'name': "Mens 4th team",
            'captain': next((m for m in mens_committee if m.position.name == "Men's 4th XI Captain"), None),
            'vice_captain': next((m for m in mens_committee if m.position.name == "Men's 4th XI Vice-Captain"), None)
        },{
            'name': "Mens 5th team",
            'captain': next((m for m in mens_committee if m.position.name == "Men's 5th XI Captain"), None),
            'vice_captain': next((m for m in mens_committee if m.position.name == "Men's 5th XI Vice-Captain"), None)
        }]

        context['season'] = season
        context['is_current_season'] = season == Season.current()
        context['season_list'] = Season.objects.all().order_by("-start")
        return context


class FeesView(TemplateView):
    """ View for displaying information about fees. Includes travel re-imbursement for away venues.
    """
    template_name='core/fees.html'

    def get_context_data(self, **kwargs):
        """
        Gets the context data for the view.

        """
        context = super(FeesView, self).get_context_data(**kwargs)

        venues = Venue.objects.away_venues().only('name', 'distance')
        context['venues'] = venues
        return context


# Fix for S3 path being incorrect:
# Ref: http://code.larlet.fr/django-storages/issue/121/s3boto-admin-prefix-issue-with-django-14
# Github issue #42
from s3_folder_storage.s3 import StaticStorage, DefaultStorage

class FixedStaticStorage(StaticStorage):

    def url(self, name):
        url = super(FixedStaticStorage, self).url(name)
        if name.endswith('/') and not url.endswith('/'):
            url += '/'
        return url

class FixedDefaultStorage(DefaultStorage):

    def url(self, name):
        url = super(FixedDefaultStorage, self).url(name)
        if name.endswith('/') and not url.endswith('/'):
            url += '/'
        return url

