import logging
from django.views.generic import TemplateView
from django.conf import settings
from core.models import ClubInfo
from matches.views import LatestResultsView, NextFixturesView
from training.views import UpcomingTrainingSessionsView

log = logging.getLogger(__name__)


class HomeView(TemplateView):
    """The main home page of the Cambridge South Hockey Club website"""
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        # Latest Results
        LatestResultsView.add_latest_results_to_context(context)

        # Next Fixtures
        NextFixturesView.add_next_fixtures_to_context(context)

        # Upcoming Training
        UpcomingTrainingSessionsView.add_upcoming_training_to_context(context)

        context['cookie_ctrl_api_key'] = settings.COOKIE_CTRL_API_KEY
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


class CommitteeView(TemplateView):
    """The main home page of the Cambridge South Hockey Club website"""
    template_name = 'core/committee.html'

    def get_context_data(self, **kwargs):
        context = super(CommitteeView, self).get_context_data(**kwargs)

        context['clubinfo'] = ClubInfo.objects.all()
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

