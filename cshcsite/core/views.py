import logging
from datetime import timedelta
from django.views.generic import TemplateView, FormView
from django.shortcuts import render_to_response
from django.contrib import messages
from django.template import RequestContext, loader, Context
from django.core.mail import send_mail, BadHeaderError
from django.utils.decorators import method_decorator
from .models import ClubInfo, ContactSubmission
from .forms import ContactSubmissionForm

log = logging.getLogger(__name__)


one_day = timedelta(days=1)
one_week = timedelta(days=7)


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
        from_email = form.cleaned_data['email']
        t = loader.get_template('core/contact_email_to_secretary.txt')
        c = Context({
            'name': "{} {}".format(form.cleaned_data['first_name'], form.cleaned_data['last_name']),
            'phone': form.cleaned_data['phone'],
            'email': from_email,
            'join_mail_list': form.cleaned_data['mailing_list'],
            'message': form.cleaned_data['message'],
        })
        subject = "Message from {}".format(c['name'])

        message = t.render(c)
        try:
            recipient_email = ClubInfo.objects.get(key='SecretaryEmail').value
        except ClubInfo.DoesNotExist:
                recipient_email = 'secretary@cambridgesouthhockeyclub.co.uk'
        send_mail(subject, message, from_email, [recipient_email], fail_silently=False)

    def email_to_enquirer(self, form):
        t = loader.get_template('core/contact_thanks_email.txt')
        c = Context({
            'first_name': form.cleaned_data['first_name'],
            'message': form.cleaned_data['message'],
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
            messages.info(self.request, "Thanks for your message. We'll be in touch shortly!")
        except BadHeaderError:
            log.warn("Failed to send email")
            messages.warning(self.request, "Sorry - we were unable to send your message. Please try again later.")
        return super(ContactSubmissionCreateView, self).form_valid(form)

    def form_invalid(self, form):
        messages.info(
            self.request,
            "Submission failed. Errors: {}".format(form.errors)
        )
        return super(ContactSubmissionCreateView, self).form_invalid(form)
