# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function

WX_TOKEN = ""
WX_USE_CACHE = False

WX_MANGER_STATES = {}


def get_conf(name, default=""):
    try:
        from django.conf import settings
        object = settings
    except Exception:
        object = __file__
    return getattr(object, name, default)