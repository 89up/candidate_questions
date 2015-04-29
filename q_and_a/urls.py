# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'constituencies.views.HomePageView', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^organisations', include('organisations.urls')),
    url(r'^candidates', include('candidates.urls')),
    url(r'^api/v1/question/(\d+)/?$', 'questions.views.api'),
    url(r'^constituencies/', include('constituencies.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
