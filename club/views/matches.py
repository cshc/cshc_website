from django.http import HttpResponse
from django.template import Context, loader
from django.shortcuts import render

def details(request, match_id):
    """ Displays the details of a particular match """
    context = Context({
        'match_id': match_id,
    })
    return render(request, 'matches/match_details.html', context)