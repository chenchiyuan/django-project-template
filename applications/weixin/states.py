# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from applications.weixin.models import App
from applications.weixin.response import MessageResponse, EventResponse
from applications.weixin.weixin.interface import StateInterface


class NoCacheState(StateInterface):
    def __init__(self, *args, **kwargs):
        super(NoCacheState, self).__init__(*args, **kwargs)

    def get_context(self):
        return {
            "from": "weixin"
        }

    def next(self, input):
        state, kwargs = super(NoCacheState, self).next(input)
        return "NO_CACHE", kwargs

    def to_xml(self, input):
        response = MessageResponse.response(input)
        return self.response_articles(response)

    def response_articles(self, response):
        if type(response) is list:
            context = self.get_context()
            return self._to_full_text(response, context=context)
        elif type(response) in (unicode, str):
            return self._to_wx_text(response)
        else:
            return self._to_wx_text("")


class MenuEventState(NoCacheState):
    def to_xml(self, input):
        response = EventResponse.response(input)
        return self.response_articles(response)


class SubscribeEventState(NoCacheState):
    def to_xml(self, input):
        app = App.only_one()
        rule = app.subscribe_rule
        if not rule:
            return self._to_wx_text("")

        response = EventResponse.response(rule.id)
        return self.response_articles(response)