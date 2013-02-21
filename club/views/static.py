from django.http import HttpResponse
from django.template import RequestContext, loader

#this is an example view just to show bootstrap working
def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render(RequestContext(request)))
