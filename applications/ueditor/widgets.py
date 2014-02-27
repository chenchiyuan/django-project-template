# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.forms import Textarea
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe


class UeditorWidget(Textarea):

    class Media:
        css = {
            "all": ('static/ueditor/themes/iframe.css'),
        }

    def __init__(self, attrs=None):
        default_attrs = {'width': '800', 'height': '600'}
        if attrs:
            default_attrs.update(attrs)
        super(UeditorWidget, self).__init__(default_attrs)

    def render(self, name, value, attrs=None):
        context = {
            "height": self.attrs.get("height", "600"),
            "width": self.attrs.get("width", "800"),
            "name": name,
            "value": value,
        }
        html = render_to_string("ueditor.html", context)
        return mark_safe(html)
