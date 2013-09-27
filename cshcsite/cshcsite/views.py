import logging
from django.views.generic import TemplateView
from django.conf import settings
from django.contrib import messages
from twython import Twython
from templated_emails.utils import send_templated_email
from core.views import AjaxGeneral, is_prod_site
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
        if is_prod_site():
            messages.warning(self.request, "No Google Calendars imported yet for the production site")
            # TODO: Set google calendar urls for production site feeds
        else:
            context['l1_gcal'] = '3r9qabjcbhh6jmfksbd3rdhldq41ss2s@import.calendar.google.com'
            context['l2_gcal'] = '2vkrhsi8la89bbc88gbvka8o0phmgdq1@import.calendar.google.com'
            context['m1_gcal'] = 'qf04nd137chqcb4sfj14iv9rqeeo8r12@import.calendar.google.com'
            context['m2_gcal'] = '8bfneiki1pl0v2dgm7dok7oeai5p545n@import.calendar.google.com'
            context['m3_gcal'] = '5ldru6voa2bfli0dt7q1afmopdts1e82@import.calendar.google.com'
            context['m4_gcal'] = '0mbj8h3g1tja0mau6vsr42lsuapjb2j3@import.calendar.google.com'
            context['m5_gcal'] = 'c5kcqb9nvg4249e4l2oi62f5r73cbch6@import.calendar.google.com'
            context['all_gcal'] = 'i7ngcunrs8icf3btp6llk1eav1bvuqol@import.calendar.google.com'
            context['training_gcal'] = '55b76kp09vmmck17985jt8qce08e9jee@import.calendar.google.com'
        return context


class CommitteeView(TemplateView):
    """The main home page of the Cambridge South Hockey Club website"""
    template_name = 'core/committee.html'

    def get_context_data(self, **kwargs):
        context = super(CommitteeView, self).get_context_data(**kwargs)

        context['clubinfo'] = ClubInfo.objects.all()
        return context


class LoadTweetsView(AjaxGeneral):
    """An Ajax-requested view for fetching the latest CSHC tweets. Uses Twython."""
    template_name = 'core/_tweets.html'

    NUM_TWEETS_TO_DISPLAY = 20

    def get_template_context(self, **kwargs):
        context = {}
        twitter = Twython(app_key=settings.TWITTER_CONSUMER_KEY,
                          app_secret=settings.TWITTER_CONSUMER_SECRET,
                          oauth_token=settings.TWITTER_OAUTH_TOKEN,
                          oauth_token_secret=settings.TWITTER_OAUTH_SECRET)

        tweets = twitter.get_user_timeline(screen_name=settings.DEFAULT_TWITTER_USER, count=LoadTweetsView.NUM_TWEETS_TO_DISPLAY, exclude_replies=True)
        context['tweets'] = [LoadTweetsView.html_for_tweet(t) for t in tweets]
        return context

    @staticmethod
    def html_for_tweet(tweet, use_display_url=True, use_expanded_url=False):
        """Return HTML for a tweet (urls, mentions, hashtags replaced with links)

        :param tweet: Tweet object from received from Twitter API
        :param use_display_url: Use display URL to represent link (ex. google.com, github.com). Default: True
        :param use_expanded_url: Use expanded URL to represent link (e.g. http://google.com). Default False

        If use_expanded_url is True, it overrides use_display_url.
        If use_display_url and use_expanded_url is False, short url will be used (t.co/xxxxx)

        """
        if 'retweeted_status' in tweet:
            tweet = tweet['retweeted_status']

        if 'entities' in tweet:
            text = tweet['text']
            entities = tweet['entities']

            # Mentions
            for entity in entities['user_mentions']:
                start, end = entity['indices'][0], entity['indices'][1]

                mention_html = '<a href="https://twitter.com/%(screen_name)s" class="twython-mention">@%(screen_name)s</a>'
                text = text.replace(tweet['text'][start:end], mention_html % {'screen_name': entity['screen_name']})

            # Hashtags
            for entity in entities['hashtags']:
                start, end = entity['indices'][0], entity['indices'][1]

                hashtag_html = '<a href="https://twitter.com/search?q=%%23%(hashtag)s" class="twython-hashtag">#%(hashtag)s</a>'
                text = text.replace(tweet['text'][start:end], hashtag_html % {'hashtag': entity['text']})

            # Urls
            for entity in entities['urls']:
                start, end = entity['indices'][0], entity['indices'][1]
                if use_display_url and entity.get('display_url') and not use_expanded_url:
                    shown_url = entity['display_url']
                elif use_expanded_url and entity.get('expanded_url'):
                    shown_url = entity['expanded_url']
                else:
                    shown_url = entity['url']

                url_html = '<a href="%s" class="twython-url">%s</a>'
                text = text.replace(tweet['text'][start:end], url_html % (entity['url'], shown_url))

        return text
