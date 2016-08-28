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
  "mixed": "Mixed",
  "indoor": "Indoor",
}

def utils(request):
    """ Returns common context items. """
    context = {'VERSION': settings.VERSION}
    team = request.COOKIES.get('cshc_team')
    if team != None:
      team_url = reverse('clubteam_detail', kwargs={'slug': team})
      context['TEAM_CONTEXT'] = team_url
      context['TEAM_CONTEXT_NAME'] = team_names[team]
    return context
