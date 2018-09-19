""" Django views that don't fit nicely into one of the other apps.
"""

from django.views.generic import TemplateView
from core.views import get_season_from_kwargs, add_season_selector
from core.models import ClubInfo, TeamGender
from competitions.models import Season
from matches.views import LatestResultsView, NextFixturesView
from training.views import UpcomingTrainingSessionsView
from members.models import CommitteeMembership
from venues.models import Venue


class HomeView(TemplateView):
    """ The main home page of the Cambridge South Hockey Club website. """
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        # Latest Results
        LatestResultsView.add_latest_results_to_context(context)

        # Next Fixtures
        NextFixturesView.add_next_fixtures_to_context(context)

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


class CalendarView(TemplateView):
    """ Displays an embedded Google Calendar view of the various fixtures, social events
        and training sessions for the current season.
    """
    template_name = 'core/calendar.html'

    def get_context_data(self, **kwargs):
        # Tip: Login to google calendar cshc.club@gmail.com (password in 'Account
        # Details' Google Doc) to get these addresses
        context = super(CalendarView, self).get_context_data(**kwargs)
        context['l1_gcal'] = '3r9qabjcbhh6jmfksbd3rdhldq41ss2s@import.calendar.google.com'
        context['l2_gcal'] = '2vkrhsi8la89bbc88gbvka8o0phmgdq1@import.calendar.google.com'
        context['l3_gcal'] = 'ls152bvh17a4h3t6920qbdg9flr2fhuo@import.calendar.google.com'
        context['l4_gcal'] = 'cf9pt1m6jjmdn0uffh2usdbulek014p3@import.calendar.google.com'
        context['m1_gcal'] = 'qf04nd137chqcb4sfj14iv9rqeeo8r12@import.calendar.google.com'
        context['m2_gcal'] = '8bfneiki1pl0v2dgm7dok7oeai5p545n@import.calendar.google.com'
        context['m3_gcal'] = '5ldru6voa2bfli0dt7q1afmopdts1e82@import.calendar.google.com'
        context['m4_gcal'] = '0mbj8h3g1tja0mau6vsr42lsuapjb2j3@import.calendar.google.com'
        context['m5_gcal'] = 'c5kcqb9nvg4249e4l2oi62f5r73cbch6@import.calendar.google.com'
        context['mv_gcal'] = 'rtnmi0btdk1fi49efro5m28elerrf1t4@import.calendar.google.com'
        context['indoor_gcal'] = 'nu45sf672k89f3m3acs093t8lnd4j4ev@import.calendar.google.com'
        context['mixed_gcal'] = '9fk8np83pe4kkodkaefl0e3stgn3sosf@import.calendar.google.com'
        context['all_gcal'] = 'i7ngcunrs8icf3btp6llk1eav1bvuqol@import.calendar.google.com'
        context['training_gcal'] = '55b76kp09vmmck17985jt8qce08e9jee@import.calendar.google.com'
        context['events_gcal'] = 't7dhl1k54rqb6mmt0huu778ac8@group.calendar.google.com'
        context['juniors_gcal'] = '4oati7ee6231hb6gtajift5hvs@group.calendar.google.com'
        return context



class CommitteeSeasonView(TemplateView):
    """ View for displaying the Club Committee members for a particular season. """
    template_name = 'core/committee.html'

    def get_context_data(self, **kwargs):
        context = super(CommitteeSeasonView, self).get_context_data(**kwargs)

        # If we're viewing this season's committee we may not have a season_slug keyword arg.
        season = get_season_from_kwargs(kwargs)

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
        },{
            'name': "Ladies 4th team",
            'captain': next((m for m in ladies_committee if m.position.name == "Ladies' 4th XI Captain"), None),
            'vice_captain': next((m for m in ladies_committee if m.position.name == "Ladies' 4th XI Vice-Captain"), None)
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

        add_season_selector(context, season, Season.objects.reversed())
        return context


class NewPlayersView(TemplateView):
    """ Display information for new players
    """
    template_name = 'core/new_players.html'

    def get_context_data(self, **kwargs):
        context = super(NewPlayersView, self).get_context_data(**kwargs)

        return context

