from django.http import HttpResponse, Http404
from django.template import RequestContext, Context, loader
from django.shortcuts import render, get_object_or_404
from club.models.match import *
from club.models.util import *

def index(request):
    return HttpResponse("Matches summary")

def details(request, match_id):
    """ Displays the details of a particular match """
    try:
        match = Match.objects.select_related('our_team', 'opp_team', 'opp_team__club', 'venue').prefetch_related('appearances', 'award_winners').get(pk=match_id)
    except Match.DoesNotExist:
        raise Http404

    same_date_matches = Match.objects.filter(date=match.date)
    
    next_match = first_or_none(Match.objects.filter(date__gt=match.date))
    prev_match = first_or_none(Match.objects.filter(date__lt=match.date))
    
    context = Context({
        'match': match,
        'same_date_matches': same_date_matches,
        'next_match': next_match,
        'prev_match': prev_match,
    })
    return render(request, 'matches/match_details.html', context)

def by_team(request, team):
    return HttpResponse("Matches by team: {}".format(team))

def by_season_and_team(request, season, team):
    return HttpResponse("Matches by season ({}) and team ({})".format(season, team))

def by_season(request, season):
    return HttpResponse("Matches by season: {}".format(season))

def by_date(request, date):
    return HttpResponse("Matches by date: {}".format(date))