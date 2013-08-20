# -*- coding: utf-8 -*-
#Copyright (C) 2011 Seán Hayes

from django.conf.urls import patterns, url
from .views import add

urlpatterns = patterns('',
	url(r'^$', add, name="feedback"),
)
