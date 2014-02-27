# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.conf.urls import patterns, url
from applications.base.views import ImageReceiverView

urlpatterns = patterns('',
    url(r'^upload/$', ImageReceiverView.as_view(), name="image_upload_view"),
)
