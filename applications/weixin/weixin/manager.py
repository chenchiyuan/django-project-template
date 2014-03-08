# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from applications.weixin.weixin.conf import get_conf
from applications.weixin.weixin.utils import get_class_by_path


class CacheMixin(object):
    def gen_cache_key(self, from_user_name, **kwargs):
        key = "USER:STATE:%s" % from_user_name
        return key

    def get_from_cache(self, from_user_name, **kwargs):
        from django.core.cache import cache
        key = self.gen_cache_key(from_user_name)
        return cache.get(key)

    def set_cache(self, from_user_name, **kwargs):
        from django.core.cache import cache
        key = self.gen_cache_key(from_user_name)
        cache.set(key, kwargs)

class StateManager(CacheMixin, object):
    """
    只负责状态切换的逻辑，Cache封装在这一层。
    """
    states = dict(map(lambda item: (item[0], get_class_by_path(item[1])),
        get_conf("WX_MANGER_STATES", {}).items()))

    def __init__(self, origin, state_name="ECHO", no_cache=False, **kwargs):
        # 如果no_cache, 默认不使用cache

        self.origin = origin
        self.use_cache = get_conf("WX_USE_CACHE") and no_cache
        state = self.initial_state(self.origin, state_name, **kwargs)
        if self.use_cache:
            # 这里从cache中获取用户当前状态
            self.now_state = None
        else:
            # 否则根据分发来的状态制定初始状态
            self.now_state = state

    @classmethod
    def initial(cls, origin, state_name, **kwargs):
        state = cls.initial_state(origin, state_name, **kwargs)
        return cls(state=state, no_cache=True, **kwargs)

    @classmethod
    def initial_state(cls, origin, state_name, **kwargs):
        if not state_name in cls.states:
            return ""
        state_cls = cls.states[state_name]
        state = state_cls(origin=origin, **kwargs)
        return state

    def get_state(self, input):
        next_state, kwargs = self.now_state.next(input)
        return self.states[next_state](origin=self.origin, **kwargs)

    def set_next(self, input):
        self.now_state = self.get_state(input)

    def handler(self, input):
        response = self.now_state.to_xml(input)
        self.set_next(input)
        return response
