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
from .serializers import MatchCommentSerializer, MatchCommentatorSerializer
from .models import MatchComment, MatchCommentator


class MatchCommentList(generics.ListCreateAPIView):
    """
    List all match comments for a particular match, only returning comments
    that have been modified after the specified date/time.

    Also handles creating (via POST) a match comment.
    """

    serializer_class = MatchCommentSerializer

    def get_queryset(self):
        match_id = self.kwargs['match_id']
        return MatchComment.objects.by_match(match_id)


class MatchCommentDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get/update/delete a particular match comment.
    """

    queryset = MatchComment.objects.all()
    serializer_class = MatchCommentSerializer


class MatchCommentatorList(generics.ListCreateAPIView):
    """
    List all match commentators for a particular match (should always be zero or one).

    Also handles creating (via POST) a match commentator.
    """

    serializer_class = MatchCommentatorSerializer

    def get_queryset(self):
        match_id = self.kwargs['match_id']
        return MatchCommentator.objects.filter(match_id=match_id)


class MatchCommentatorDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Get/update/delete a particular match comment.
    """

    queryset = MatchCommentator.objects.all()
    serializer_class = MatchCommentatorSerializer
