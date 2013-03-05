import logging
from exceptions import IndexError
from django.http import HttpResponse, Http404
from django.template import RequestContext, Context, loader
from django.shortcuts import render, get_object_or_404
from datetime import datetime, date
from club.models.club import Club
from club.models.match import *
from club.models.award import MatchAwardWinner
from club.models.util import *

logger = logging.getLogger(__name__)

def index(request):
    return HttpResponse("Matches summary")


def details(request, match_id):
    """ Displays the details of a particular match """

    try:
        match = Match.objects.select_related('our_team__club', 'opp_team__club', 'venue').get(pk=match_id)
    except Match.DoesNotExist:
        raise Http404

    # TODO: Tidy this up, amalgamate calls to DB.
    same_date_matches = Match.objects.filter(date=match.date).exclude(pk=match_id)
    
    award_winners = match.award_winners.select_related('award', 'player').all()
    appearances = match.appearances.select_related('player').all()

    prev_match = first_or_none(Match.objects.select_related('our_team__club', 'opp_team__club').order_by('-date').filter(our_team=match.our_team, date__lt=match.date))
    
    next_match = first_or_none(Match.objects.select_related('our_team__club', 'opp_team__club').filter(our_team=match.our_team, date__gt=match.date))

    context = Context({
        'match': match,
        'award_winners': award_winners,
        'appearances': appearances,
        'same_date_matches': same_date_matches,
        'next_match': next_match,
        'prev_match': prev_match,
        'venue': match.venue
    })
    return render(request, 'matches/match_details.html', context)


def by_team(request, gender, ordinal):
    """ Displays all matches for a particular team (for the current season). """
    # TODO: Avoid retrieving season twice (see by_season_and_team as well)
    season = Season.current()
    return by_season_and_team(request, season.start.year, gender, ordinal)


def by_season_and_team(request, year, gender, ordinal):
    """ Displays all matches for a particular team in a particular season."""
    jan1st = date(int(year), 1, 1)
    try:
        season = Season.objects.filter(start__gte=jan1st)[0]
    except IndexError: 
        raise Http404
    try:
        team = Team.objects.get(gender__iexact=gender, ordinal__iexact=ordinal, club=Club.our_club())
    except Team.DoesNotExist:
        raise Http404
    matches = Match.objects.select_related('our_team__club', 'opp_team__club', 'venue').filter(our_team=team, date__gte=season.start, date__lte=season.end)
    context = Context({
        'season': season,
        'team': team,
        'matches': matches
    })
    return render(request, 'matches/matches_by_team_season.html', context)


def by_season(request, year):
    """ Displays all matches for a particular season. """
    jan1st = date(int(year), 1, 1)
    logging.debug("jan1st = {}".format(jan1st))
    try:
        season = Season.objects.filter(start__gte=jan1st)[0]
    except IndexError: 
        raise Http404
    
    matches = Match.objects.select_related('our_team__club', 'opp_team__club', 'venue').filter(date__gte=season.start, date__lte=season.end)
    context = Context({
        'season': season,
        'matches': matches
    })
    return render(request, 'matches/matches_by_season.html', context)


def by_date(request, date):
    """ Displays all matches on a particular date. """
    d = datetime.strptime(date, '%d-%b-%Y').date()
    matches = Match.objects.filter(date=d)
    context = Context({
        'date': d,
        'matches': matches
    })
    return render(request, 'matches/matches_by_date.html', context)