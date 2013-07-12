import logging
from datetime import datetime, date, timedelta
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils.decorators import method_decorator
from .models import ClubInfo

logger = logging.getLogger(__name__)


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
    return dict.has_key(key) and dict[key] != None and dict[key] != ""


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
    template_name= None

    def get(self, request, *args, **kwargs):
        data=self.get_template_context(**kwargs)
        return render_to_response(self.template_name, data,
            context_instance=RequestContext(request))

    def get_template_context(self, **kwargs):
        msg = "{0} is missing get_template_context.".format(self.__class__)
        raise NotImplementedError(msg)

    @method_decorator(ajax_request)
    def dispatch(self, *args, **kwargs):
        return super(AjaxGeneral, self).dispatch(*args, **kwargs)
