# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from collections import OrderedDict
from applications.weixin.models.apps import App
from applications.weixin.models.rules import Rule
from libs.models.mixins import QuerysetMixin
from libs.models.models import SingletonModel
from django.db import models


class SubscribeItem(SingletonModel, QuerysetMixin):
    class Meta:
        app_label = "weixin"
        db_table = "weixin_subscribe"
        verbose_name = verbose_name_plural = u"微信关注回复"

    app = models.ForeignKey(App, verbose_name=u"app")
    rule = models.ForeignKey(Rule, verbose_name=u"对应关键字")

    def __unicode__(self):
        return self.id


class MenuItem(models.Model, QuerysetMixin):
    class Meta:
        app_label = "weixin"
        db_table = "weixin_menu"
        verbose_name = verbose_name_plural = u"微信菜单"

    main = models.CharField(u"主菜单", max_length=64)
    secondary = models.CharField(u"二级菜单", max_length=64, blank=True, null=True)
    app = models.ForeignKey(App, verbose_name=u"app")

    rule = models.ForeignKey(Rule, verbose_name=u"对应关键字", blank=True, null=True)
    link = models.CharField(u"链接", max_length=128, blank=True, null=True)

    def __unicode__(self):
        return self.id

    @classmethod
    def get_menus_by_app(cls, app):
        menus = cls.filter_by_queries(app=app)
        menu_dict = OrderedDict()
        for menu in menus:
            if not menu.main in menu_dict:
                menu_dict[menu.main] = []
            menu_dict[menu.main].append(menu)

        top_three_menus = menu_dict.items()[:3]
        result = {
            "button": []
        }

        for menu_main, menu_items in top_three_menus:
            if len(menu_items) == 1:
                # 一个的时候需要判断下
                result_item = menu_items[0].to_button()
                result['button'].append(result_item)
            else:
                sub_buttons = []
                for menu_item in menu_items:
                    sub_buttons.append(menu_item.to_button())
                result['button'].append({
                    "name": menu_main,
                    "sub_button": sub_buttons
                })
        return result


    @property
    def name(self):
        if self.secondary:
            return self.secondary
        return self.main

    def to_button(self):
        if self.link:
            return {
                "type": "view",
                "name": self.name,
                "url": self.link
            }
        else:
            return {
                "type": "click",
                "name": self.name,
                "key": unicode(self.rule_id)
            }