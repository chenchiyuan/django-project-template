# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
import imghdr


def detect_image_type(content):
    return imghdr.what("", h=content)