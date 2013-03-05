import logging
from django.http import HttpResponse, Http404
from django.template import RequestContext, Context, loader
from django.shortcuts import render, get_object_or_404
from datetime import datetime, date
from club.models.venue import Venue

logger = logging.getLogger(__name__)

def index(request):

    venues = Venue.objects.all()
    context = Context({
        'venues': venues,
    })
    return render(request, 'venues/venues_summary.html', context)

def details(request, venue_short_name):
    """ Displays the details of a particular venue """
    try:
        venue = Venue.objects.get(short_name__iexact=venue_short_name.replace("-", " "))
    except Venue.DoesNotExist:
        raise Http404
    
    context = Context({
        'venue': venue,
    })
    return render(request, 'venues/venue_details.html', context)