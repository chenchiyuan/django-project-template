# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.db import models
from libs.models.mixins import QuerysetMixin


class Rule(models.Model, QuerysetMixin):
    class Meta:
        app_label = "weixin"
        db_table = "weixin_rule"
        verbose_name = verbose_name_plural = "关键字"

    text = models.CharField(u"关键字", max_length=64)
    response = models.TextField(u"文字回复", max_length=1024, blank=True, null=True,
                                help_text="如果有关联的图文消息，则不显示该段文字。",)

    def __unicode__(self):
        return self.text

    @classmethod
    def get_rule(cls, text):
        rule = cls.get_by_queries(**{"text": text})
        return rule

    def to_articles(self):
        rts = self.richtext_set.all()
        if not rts:
            return self.response

        articles = []
        for rich_text in rts:
            articles.append(rich_text.to_article())
        return articles
