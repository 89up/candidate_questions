# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from constituencies.views import ConstituencyView

urlpatterns = patterns('',
    url(r'^(\d+)/$', ConstituencyView.as_view(), name='constituency'),
)
