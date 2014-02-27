# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
import urllib
import urlparse


def get_class_by_path(name):
    components = name.split('.')
    mod = __import__(".".join(components[:-1]))
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod


def merge_url(url, context={}):
    try:
        parsed = urlparse.urlparse(url)
        query = parsed.query

        if query:
            base_dict = dict(map(lambda item: (item.split("=")), query.split("&")))
            final_dict = dict(context.items() + base_dict.items())
        else:
            final_dict = context

        final_query = urllib.urlencode(final_dict)
        new_parsed_url = urlparse.ParseResult(scheme=parsed.scheme, netloc=parsed.netloc,
                                              path=parsed.path, params=parsed.params, query=final_query,
                                              fragment=parsed.fragment)
        return new_parsed_url.geturl()
    except:
        return ""