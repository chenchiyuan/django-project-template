# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from applications.weixin.models import Rule, RichText


class QueryResponse(object):
    @classmethod
    def response_texts(cls, queryset):
        articles = []
        for rich_text in queryset:
            articles.append(rich_text.to_article())
        return articles[:10]


class ResponseBase(object):
    max_count = 9

    @classmethod
    def get_rule(cls, input):
        rule = Rule.get_rule(input)
        return rule

    @classmethod
    def get_rule_by_pk(cls, input):
        rule = Rule.get_by_unique(id=input)
        return rule

    @classmethod
    def _response_rule_queryset(cls, rule, queryset):
        if queryset.count():
            return QueryResponse.response_texts(queryset[:cls.max_count])
        elif rule:
            return rule.response
        else:
            return ""

    @classmethod
    def get_queryset(cls, input):
        raise NotImplemented

    @classmethod
    def response(cls, input):
        raise NotImplemented


class MessageResponse(ResponseBase):
    @classmethod
    def get_queryset(cls, input):
        rule = cls.get_rule(input)
        if not rule:
            queryset = RichText.filter_by_queries(
                title__icontains=input,
            )
            return queryset
        else:
            queryset = rule.richtext_set.all()
            return queryset

    @classmethod
    def response(cls, input):
        rule = cls.get_rule(input)
        queryset = cls.get_queryset(input)
        response = cls._response_rule_queryset(rule, queryset)
        return response


class EventResponse(ResponseBase):
    @classmethod
    def response(cls, input):
        rule = cls.get_rule_by_pk(input)
        queryset = cls.get_queryset(input)
        response = cls._response_rule_queryset(rule, queryset)
        return response

    @classmethod
    def get_queryset(cls, input):
        rule = cls.get_rule_by_pk(input)
        queryset = rule.richtext_set.all()
        return queryset
