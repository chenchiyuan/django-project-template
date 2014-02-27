# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.conf.urls import patterns, url
from views import ImageUploadView

urlpatterns = patterns('',
    url(r'^image/upload/$', ImageUploadView.as_view(), name="ueditor_image_upload"),
)
