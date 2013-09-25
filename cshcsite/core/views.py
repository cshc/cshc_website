import logging
from datetime import timedelta
from django.views.generic import TemplateView, FormView
from django.shortcuts import render_to_response
from django.contrib import messages
from django.template import RequestContext
from django.contrib.sites.models import Site
from django.conf import settings
from django.utils.decorators import method_decorator
from django.contrib.sites.models import RequestSite
from templated_emails.utils import send_templated_email
from registration import signals as reg_signals
from registration.views import RegistrationView as BaseRegistrationView
from .models import ClubInfo, ContactSubmission
from .forms import ContactSubmissionForm, UserCreationForm
from .reg_utils import create_inactive_user

log = logging.getLogger(__name__)


one_day = timedelta(days=1)
one_week = timedelta(days=7)


def is_prod_site():
    return 'cambridgesouthhockeyclub' in Site.objects.all()[0].domain

def saturdays_in_season(season):
    """ Gets a list of all the Saturdays (match days) in the given season. """
    return saturdays_in_range(season.start, season.end)


def saturdays_in_range(start, end):
    """ Gets a list of all the Saturdays (match days) in the given range. """
    sats = []
    sat = _first_sat(start)
    while sat <= end:
        sats.append(sat)
        sat += one_week

    return sats


def _first_sat(dt):
    """ Gets the first Saturday following the given date. """
    while dt.weekday() < 5:
        dt = dt + one_day
    return dt


def valid_kwarg(key, **dict):
    """Given a key and a dictionary, returns True if the given key is in the dictionary and its value is not None or an empty string"""
    return key in dict and dict[key] is not None and dict[key] != ""


def kwargs_or_none(key, **dict):
    """Given a key and a dictionary, returns the key's value, or None if the key is not valid"""
    if(valid_kwarg(key, **dict)):
        return dict[key]
    else:
        return None


def add_clubinfo_to_context(context):
    context['clubinfo'] = ClubInfo.objects.all()


def ajax_request(function):
    """
    Used as a method decorator.
    Given a request, checks if the request is an AJAX request.
    If not, the 'AJAX required' error template is rendered.
    Otherwise the wrapped function is called.
    """
    def wrapper(request, *args, **kwargs):
        if not request.is_ajax():
            return render_to_response('error/ajax_required.html', {},
                                      context_instance=RequestContext(request))
        else:
            return function(request, *args, **kwargs)
    return wrapper


class AjaxGeneral(TemplateView):
    """
    Base template view for AJAX views.
    All views are wrapped by a call that ensures the request is an AJAX request.
    """
    template_name = None

    def get(self, request, *args, **kwargs):
        data = self.get_template_context(**kwargs)
        return render_to_response(self.template_name, data,
                                  context_instance=RequestContext(request))

    def get_template_context(self, **kwargs):
        msg = "{0} is missing get_template_context.".format(self.__class__)
        raise NotImplementedError(msg)

    @method_decorator(ajax_request)
    def dispatch(self, *args, **kwargs):
        return super(AjaxGeneral, self).dispatch(*args, **kwargs)


class ContactSubmissionCreateView(FormView):
    """This is essentially the 'Contact Us' form view"""
    model = ContactSubmission
    form_class = ContactSubmissionForm
    template_name = "core/contact.html"
    # TODO: Redirect to another page and give them more links to click on!
    success_url = '/contact/'

    def email_to_secretary(self, form):
        email = form.cleaned_data['email']
        context = {
            'name': "{} {}".format(form.cleaned_data['first_name'], form.cleaned_data['last_name']),
            'phone': form.cleaned_data['phone'],
            'email': email,
            'join_mail_list': form.cleaned_data['mailing_list'],
            'message': form.cleaned_data['message'],
        }

        try:
            recipient_email = ClubInfo.objects.get(key='SecretaryEmail').value
        except ClubInfo.DoesNotExist:
                recipient_email = 'secretary@cambridgesouthhockeyclub.co.uk'
        send_templated_email([recipient_email], 'emails/contact_secretary', context)

    def email_to_enquirer(self, form):
        context = {
            'first_name': form.cleaned_data['first_name'],
            'message': form.cleaned_data['message'],
        }
        try:
            context['secretary_name'] = ClubInfo.objects.get(key='SecretaryName').value
            context['secretary_email'] = ClubInfo.objects.get(key='SecretaryEmail').value
        except ClubInfo.DoesNotExist:
            context['secretary_name'] = ""
            context['secretary_email'] = 'secretary@cambridgesouthhockeyclub.co.uk'

        recipient_email = form.cleaned_data['email']
        send_templated_email([recipient_email], 'emails/contact_sender', context)

    def form_valid(self, form):
        try:
            self.email_to_secretary(form)
            self.email_to_enquirer(form)
            messages.info(self.request, "Thanks for your message. We'll be in touch shortly!")
        except:
            log.warn("Failed to send contact us email")
            messages.error(self.request, "Sorry - we were unable to send your message. Please try again later.")
        return super(ContactSubmissionCreateView, self).form_valid(form)



# Copied and modified from registration.backends.default.views
class RegistrationView(BaseRegistrationView):
    """
    A registration backend which follows a simple workflow:

    1. User signs up, inactive account is created.

    2. Email is sent to user with activation link.

    3. User clicks activation link, account is now active.

    Using this backend requires that

    * ``registration`` be listed in the ``INSTALLED_APPS`` setting
      (since this backend makes use of models defined in this
      application).

    * The setting ``ACCOUNT_ACTIVATION_DAYS`` be supplied, specifying
      (as an integer) the number of days from registration during
      which a user may activate their account (after that period
      expires, activation will be disallowed).

    * The creation of the templates
      ``registration/activation_email_subject.txt`` and
      ``registration/activation_email.txt``, which will be used for
      the activation email. See the notes for this backends
      ``register`` method for details regarding these templates.

    Additionally, registration can be temporarily closed by adding the
    setting ``REGISTRATION_OPEN`` and setting it to
    ``False``. Omitting this setting, or setting it to ``True``, will
    be interpreted as meaning that registration is currently open and
    permitted.

    Internally, this is accomplished via storing an activation key in
    an instance of ``registration.models.RegistrationProfile``. See
    that model and its custom manager for full documentation of its
    fields and supported operations.

    """

    form_class = UserCreationForm

    def register(self, request, **cleaned_data):
        """
        Given an email address, first and last name and password, register a new
        user account, which will initially be inactive.

        Along with the new ``User`` object, a new
        ``registration.models.RegistrationProfile`` will be created,
        tied to that ``User``, containing the activation key which
        will be used for this account.

        An email will be sent to the supplied email address; this
        email should contain an activation link. The email will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.send_activation_email()`` for
        information about these templates and the contexts provided to
        them.

        After the ``User`` and ``RegistrationProfile`` are created and
        the activation email is sent, the signal
        ``registration.signals.user_registered`` will be sent, with
        the new ``User`` as the keyword argument ``user`` and the
        class of this backend as the sender.

        """
        email, first_name, last_name, password = cleaned_data['email'], cleaned_data['first_name'], cleaned_data['last_name'], cleaned_data['password1']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
        new_user = create_inactive_user(email, password, first_name, last_name, site)
        reg_signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        return new_user

    def registration_allowed(self, request):
        """
        Indicate whether account registration is currently permitted,
        based on the value of the setting ``REGISTRATION_OPEN``. This
        is determined as follows:

        * If ``REGISTRATION_OPEN`` is not specified in settings, or is
          set to ``True``, registration is permitted.

        * If ``REGISTRATION_OPEN`` is both specified and set to
          ``False``, registration is not permitted.

        """
        return getattr(settings, 'REGISTRATION_OPEN', True)

    def get_success_url(self, request, user):
        """
        Return the name of the URL to redirect to after successful
        user registration.

        """
        return ('registration_complete', (), {})

