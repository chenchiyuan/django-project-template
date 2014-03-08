# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
import logging
from applications.weixin.weixin.core import WeiXin

logger = logging.getLogger(__name__)


class StateInterface(object):
    """
    1. 状态根据输入决定下一个状态是什么,以及下一个状态的初始值
    2. 决定如何应答。
    状态的切换交由StateManager管理, 状态只负责处理自己的业务逻辑
    """

    def __init__(self, origin, from_user_name, to_user_name, **kwargs):
        super(StateInterface, self).__init__()

        self.origin = origin
        self.from_user_name = from_user_name
        self.to_user_name = to_user_name
        for key, value in kwargs.items():
            setattr(self, key, value)

    def __getattribute__(self, item):
        try:
            return super(StateInterface, self).__getattribute__(item)
        except Exception, err:
            logger.info(err)
            return ""

    def to_xml(self, input, *args, **kwargs):
        return ""

    def _to_wx_text(self, content=""):
        wx = WeiXin()
        xml = wx.to_text(
            from_user_name=self.from_user_name, to_user_name=self.to_user_name, content=content
        )
        return xml

    def _to_full_text(self, articles, context={}):
        wx = WeiXin()
        xml = wx.to_pic_text(
            from_user_name=self.from_user_name, to_user_name=self.to_user_name,
            articles=articles, context=context
        )
        return xml

    def next(self, input, *args, **kwargs):
        return "", {
            "from_user_name": self.from_user_name,
            "to_user_name": self.to_user_name
        }