import logging
from datetime import timedelta
from django.views.generic import TemplateView, FormView, CreateView
from django.shortcuts import render_to_response
from django.contrib import messages
from django.template import RequestContext
from django.contrib.sites.models import Site
from django.utils.decorators import method_decorator
from templated_emails.utils import send_templated_email
from .models import ClubInfo, ContactSubmission, CshcUser
from .forms import ContactSubmissionForm, UserCreationForm

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

    def form_invalid(self, form):
        messages.error(
            self.request,
            "Submission failed. Errors: {}".format(form.errors)
        )
        return super(ContactSubmissionCreateView, self).form_invalid(form)


class RegisterUserView(CreateView):

    model = CshcUser
    form_class = UserCreationForm

    template_name = "registration/register_new_user.html"
    # TODO: Redirect to a new view with a welcome message
    success_url = '/'
