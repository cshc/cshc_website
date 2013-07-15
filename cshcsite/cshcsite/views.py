import logging
from django.views.generic import TemplateView
from django.views.generic.edit import FormView
from django.contrib import messages
from django.template import loader, Context
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from twython import Twython
from braces.views import LoginRequiredMixin, SuperuserRequiredMixin
from core.views import AjaxGeneral
from core.models import ClubInfo
from matches.views import LatestResultsView, NextFixturesView
from training.views import UpcomingTrainingSessionsView
from .forms import ContactForm

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

        return context


class ContactUsView(FormView):
    """This is essentially the 'Join Us' form view"""
    form_class = ContactForm
    template_name = "core/contact.html"
    success_url = '/contact/'

    def send_email(self, form):
        from_email = form.cleaned_data['email']
        name = form.cleaned_data['name']
        subject = "Message from {}: {}".format(name, form.cleaned_data['subject'])
        message = form.cleaned_data('message')

        try:
            recipient_email = ClubInfo.objects.get(key='SecretaryEmail').value
        except ClubInfo.DoesNotExist:
                recipient_email = 'secretary@cambridgesouthhockeyclub.co.uk'
        send_mail(subject, message, from_email, [recipient_email], fail_silently=False)

    def form_valid(self, form):
        try:
            self.send_email(form)
            messages.info(self.request, "Thanks for your message. We'll be in touch shortly!")
        except BadHeaderError:
            log.warn("Failed to send email")
            messages.warning(self.request, "Sorry - we were unable to send your message. Please try again later.")
        return super(ContactUsView, self).form_valid(form)

    def form_invalid(self, form):
        messages.info(
            self.request,
            "Submission failed. Errors: {}".format(form.errors)
        )
        return super(ContactUsView, self).form_invalid(form)


class AboutUsView(TemplateView):
    """Background and History"""
    template_name = 'core/about_us.html'

    def get_context_data(self, **kwargs):
        context = super(AboutUsView, self).get_context_data(**kwargs)

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

    NUM_TWEETS_TO_DISPLAY = 10

    def get_template_context(self, **kwargs):
        context = {}
        twitter = Twython(app_key=settings.TWITTER_CONSUMER_KEY,
                          app_secret=settings.TWITTER_CONSUMER_SECRET,
                          oauth_token=settings.TWITTER_OAUTH_TOKEN,
                          oauth_token_secret=settings.TWITTER_OAUTH_SECRET)

        tweets = twitter.get_user_timeline(screen_name=settings.DEFAULT_TWITTER_USER)
        context['tweets'] = [LoadTweetsView.html_for_tweet(t) for t in tweets[:LoadTweetsView.NUM_TWEETS_TO_DISPLAY]]
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

class DataMigrationAdminView(LoginRequiredMixin, SuperuserRequiredMixin, TemplateView):
    """A temporary view to assist in migrating data from the old Access database to the new database."""
    template_name = 'core/data_migration.html'