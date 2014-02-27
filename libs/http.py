# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.http import HttpResponse
import json


def json_response(json_data, **kwargs):
    data = json.dumps(json_data)
    return HttpResponse(data, content_type='application/json', **kwargs)