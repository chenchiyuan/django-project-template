# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
import uuid


def get_uuid():
    u = uuid.uuid4()
    return str(u).replace("-", "")


def make_uuid():
    return get_uuid()
