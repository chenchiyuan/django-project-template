# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.conf import settings
from urlparse import urlparse


def replace_image(url, **kwargs):
    try:
        hosts = settings.IMG_AVAILABLE_HOSTS
        if url.startswith("/media"):
            url = settings.APP_HOST_NAME + url
        o = urlparse(url)
        host = o.netloc

        if host in hosts:
            return url

        return save_image(url, **kwargs)
    except:
        return url


def save_image(url, **kwargs):
    from models import Photo
    import requests
    o = urlparse(url)
    host = o.netloc

    headers = {
        'HTTP_REFERER': host
    }

    response = requests.get(url, headers=headers)
    photo = Photo.create_photo(response.content, name="", **kwargs)
    return photo.url
