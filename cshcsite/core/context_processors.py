""" Context processors for the CSHC website.

    Provides common key/value pairs that will be added to the
    context of all requests.

    Ref: https://docs.djangoproject.com/en/1.6/ref/templates/api/#writing-your-own-context-processors

    Note: This requires the following TEMPLATE_CONTEXT_PROCESSOR:
        'core.context_processors.utils'
"""

from django.conf import settings
from django.core.urlresolvers import reverse

team_names = {
  "m1": "#MWon",
  "m2": "Mens 2nds",
  "m3": "Mens 3rds",
  "m4": "Mens 4ths",
  "m5": "Mens 5ths",
  "l1": "Ladies 1sts",
  "l2": "Ladies 2nds",
  "l3": "Ladies 3rds",
  "l4": "Ladies 4ths",
  "mixed": "Mixed",
  "indoor": "Indoor",
  "mv": "Vets",
}

def utils(request):
    """ Returns common context items. """
    context = {
      'VERSION': settings.VERSION,
      'GMAPS_API_KEY': settings.GEOPOSITION_GOOGLE_MAPS_API_KEY,
    }
    team = request.COOKIES.get('cshc_team')
    if team != None:
      try:
        team_url = reverse('clubteam_detail', kwargs={'slug': team})
        context['TEAM_CONTEXT'] = team_url
        context['TEAM_CONTEXT_NAME'] = team_names[team]
      except:
        pass
    return context
