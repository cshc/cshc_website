import ast
import json
import time
import calendar
from datetime import datetime, date, timedelta
from django.http import HttpResponse
from django.template import RequestContext
from django.views.generic import View
from django.shortcuts import render_to_response
from rest_framework import generics
from core.views import kwargs_or_none
from .serializers import MatchCommentSerializer
from .models import MatchComment

class LatestMatchCommentsView(View):

    def get(self, args, **kwargs):
        if not self.request.is_ajax():
            return render_to_response('error/ajax_required.html', {},
                                      context_instance=RequestContext(self.request))
        match_id = kwargs['match_id']
        last_update = kwargs_or_none('last_update', **kwargs)
        if last_update:
            last_update = float(last_update)
            dt_last_update = datetime.utcfromtimestamp(time.mktime(time.gmtime(last_update)))
            new_comments = MatchComment.objects.since(match_id, dt_last_update)
        else:
            new_comments = MatchComment.objects.by_match(match_id)

        if new_comments.exists():
            updated = datetime.utcnow()
        else:
            updated = None

        result = {
            "last_update": calendar.timegm(updated.timetuple()) if updated else None,
            "comments": ast.literal_eval(serializers.serialize('json', new_comments))
        }
        return HttpResponse(json.dumps(result), content_type="application/json")



class MatchCommentList(generics.ListCreateAPIView):
    """
    List all match comments for a particular match, only returning comments
    that have been modified after the specified date/time.

    Also handles creating (via POST) a match comment.
    """

    def get_queryset(self):
        match_id = self.kwargs['match_id']
        last_update = kwargs_or_none('last_update', **self.kwargs)
        if last_update:
            # Last update is in milliseconds since the epoch
            dt_last_update = datetime.utcfromtimestamp(last_update/1000)
            print "Last comment update: " + dt_last_update
            return MatchComment.objects.since(match_id, dt_last_update)
        else:
            comments = MatchComment.objects.by_match(match_id)
            print "Fetched {} comments".format(comments.count())
            return comments

    serializer_class = MatchCommentSerializer


class MatchCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get/update/delete a particular match comment.
    """

    queryset = MatchComment.objects.all()
    serializer_class = MatchCommentSerializer
