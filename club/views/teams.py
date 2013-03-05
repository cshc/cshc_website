import logging
from django.http import HttpResponse, Http404
from django.template import RequestContext, Context, loader
from django.shortcuts import render, get_object_or_404
from datetime import datetime, date
from club.models.team import Team
from club.models.club import Club

logger = logging.getLogger(__name__)

def index(request):

    our_teams = Team.our_teams.select_related('club').all()
    context = Context({
        'our_teams': our_teams,
    })
    return render(request, 'teams/teams_summary.html', context)

def details(request, gender, ordinal):
    """ Displays the details of a particular team """
    try:
        team = Team.objects.get(gender__iexact=gender, ordinal__iexact=ordinal, club=Club.our_club())
    except Team.DoesNotExist:
        raise Http404
    
    context = Context({
        'team': team,
    })
    return render(request, 'teams/team_details.html', context)