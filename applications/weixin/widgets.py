# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.contrib.admin.widgets import ForeignKeyRawIdWidget
from django.forms import ClearableFileInput
from django.utils.safestring import mark_safe
from django.conf import settings
from applications.weixin.models import Photo


class UpyunImageWidget(ClearableFileInput):
    def render(self, name, value, attrs=None):
        template = super(UpyunImageWidget, self).render(name, value, attrs)
        url = "%s%s" % (settings.IMG_HOST, value)

        append = '<p>%s</p><a href="%s" target="_blank"><img src="%s" width="100" height="100"></a>' % (value, url, url)
        return mark_safe(template + append)


class ForeighUpyunImageWidget(ForeignKeyRawIdWidget):
    def render(self, name, value, *args, **kwargs):
        template = super(ForeighUpyunImageWidget, self).render(name, value, *args, **kwargs)
        photo = Photo.get_by_unique(id=value)
        if not photo:
            return template

        url = photo.url
        append = '<p>%s</p><a href="%s" target="_blank"><img src="%s" width="100" height="100"></a>' % (photo.name, url, url)
        return mark_safe(template + append)