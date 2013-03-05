import logging
from django.http import HttpResponse, Http404
from django.template import RequestContext, Context, loader
from django.shortcuts import render_to_response

logger = logging.getLogger(__name__)

def index(request):
    return render_to_response('calendar/main_calendar.html')