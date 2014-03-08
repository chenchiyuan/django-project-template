# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.db import models
from libs.models.models import SingletonModel
from django.conf import settings
from libs.uuids import get_uuid
import requests
import json


class App(SingletonModel):

    class Meta:
        app_label = "weixin"
        db_table = "weixin_app"
        verbose_name_plural = verbose_name = u"账号设置"

    name = models.CharField("微信名", max_length=64, default="", blank=True, null=True)
    app_url = models.CharField("微信回调地址", max_length=256, blank=True, null=True)
    app_token = models.CharField("微信Token", max_length=64, blank=True, null=True)

    app_key = models.CharField("app_key", max_length=64, blank=True, null=True)
    app_id = models.CharField("app_secret", max_length=64, blank=True, null=True)

    def __unicode__(self):
        return bool(self.name) and self.name or self.owner.email

    @property
    def subscribe_rule(self):
        subscribe = self.subscribeitem_set.all()
        if not subscribe.count():
            return None
        else:
            return subscribe[0].rule

    def get_app_url(self):
        return "%s/weixin/callback/" % settings.APP_HOST_NAME

    def save(self, force_insert=False, force_update=False, using=None):
        if force_insert and force_update:
            raise ValueError("Cannot force both insert and updating in model saving.")

        if not self.app_url:
            self.app_url = self.get_app_url()
        if not self.app_token:
            self.app_token = get_uuid()

        if self.app_key and self.app_id:
            self.delete_menus()
            self.create_menus()

        super(App, self).save(force_insert, force_update, using)

    def get_access_token(self):
        if not any([self.app_key, self.app_id]):
            raise Exception(u"必须申请app_key和app_secret".encode("utf-8"))
        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" \
              % (self.app_key, self.app_id)
        response = requests.get(url)
        json_data = json.loads(response.content)
        return json_data['access_token']

    def create_menus(self):
        from applications.weixin.models.menus import MenuItem
        token = self.get_access_token()
        post_dict = MenuItem.get_menus_by_app(self)
        headers = {'content-type': 'application/json'}

        url = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % token
        return requests.post(url, data=json.dumps(post_dict, ensure_ascii=False).encode("utf-8"), headers=headers)

    def delete_menus(self):
        token = self.get_access_token()
        url = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % token
        return requests.get(url)