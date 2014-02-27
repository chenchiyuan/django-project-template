# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.db.models import Q


class QuerysetMixin(object):
    @classmethod
    def get_by_unique(cls, **kwargs):
        try:
            instance = cls.objects.get(**kwargs)
        except Exception, err:
            print(err)
            instance = None
        return instance

    @classmethod
    def get_by_queries(cls, **kwargs):
        query_list = [Q(**{key: value}) for key, value in kwargs.items()]
        query = query_list.pop()
        for query_append in query_list:
            query &= query_append

        try:
            item = cls.objects.get(query)
        except Exception:
            item = None
        return item

    @classmethod
    def filter_by_queries(cls, **kwargs):
        query_list = [Q(**{key: value}) for key, value in kwargs.items()]
        query = query_list.pop()
        for query_append in query_list:
            query &= query_append

        try:
            item = cls.objects.filter(query)
        except Exception:
            item = cls.objects.none()
        return item