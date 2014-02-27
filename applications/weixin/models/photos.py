# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.core.files.base import ContentFile
from django.db import models
from applications.ueditor.fields import UEditorField
from applications.weixin.libs.formatters import BasicFormatter
from applications.weixin.models.rules import Rule
from libs.hashs import md5
from libs.models.mixins import QuerysetMixin
from django.conf import settings
from libs.models.storages import UpyunStorage
import os


def upload_to(instance, filename):
    return os.path.join('photos', filename)


def image_upload_to(instant, filename):
    return instant.md5 + ".jpg"


class Photo(models.Model, QuerysetMixin):
    class Meta:
        app_label = "weixin"
        db_table = "weixin_photo"
        verbose_name = verbose_name_plural = u"图片"

    md5 = models.CharField(u"MD5", max_length=64, blank=True, unique=True)
    name = models.CharField(u"图片名", max_length=64, blank=True, null=True, default="", db_index=True)
    image = models.ImageField(u"图片", storage=UpyunStorage(), upload_to=image_upload_to)

    def __unicode__(self):
        return self.name

    @property
    def filename(self):
        return image_upload_to(self, self.md5)

    @property
    def url(self):
        return self.image.url

    @classmethod
    def create_photo(cls, content, name="", **kwargs):
        m = md5(content)

        photo_instance = cls(md5=m, name=name, **kwargs)
        photo_instance.image.save(
            m,
            ContentFile(content),
            save=False
        )
        photo_instance.save()
        return photo_instance

    def read(self):
        return self.image.storage.read(self.filename)

    def save(self, force_insert=False, force_update=False, using=None):
        content = self.image.read()
        if not content:
            raise Exception("No Image Content")

        md5_sign = md5(content)
        self.md5 = md5_sign

        exists_item = Photo.get_by_queries(md5=self.md5)
        if exists_item:
            self = exists_item

        self.image.save(
            self.md5,
            ContentFile(content),
            save=False,
        )
        super(Photo, self).save(force_insert, force_update, using)




class RichText(models.Model, QuerysetMixin):
    class Meta:
        app_label = "weixin"
        db_table = "weixin_richtext"
        verbose_name = verbose_name_plural = u"图文消息"
        ordering = ['-priority']

    title = models.CharField(u"标题", max_length=64, help_text="标题", db_index=True)

    description = models.CharField(u"摘要", max_length=256, blank=True, null=True, help_text="摘要")
    photo = models.ForeignKey(Photo, verbose_name="封面图片")
    rules = models.ManyToManyField(Rule, verbose_name=u"关键字", help_text=u"匹配到的关键字",
                                   blank=True, null=True)
    link = models.CharField(u"链接", max_length=1024, blank=True, null=True,
                            help_text="添加链接后不显示正文内容，直接跳转到该链接。")
    priority = models.IntegerField(u"优先级", default=0, blank=True, null=True,
                                   help_text=u"数字越大，显示越靠前", )

    html = UEditorField(u"正文", default="", blank=True, null=True)

    def __unicode__(self):
        return self.title

    @property
    def smart_link(self):
        if self.link:
            return self.link
        return "%s/weixin/texts/%s/" % (settings.APP_HOST_NAME, self.id)


    @property
    def footer_templates(self):
        templates = self.templates.all()
        html = ''
        for template in templates:
            html += template.to_html()
        return html

    @property
    def short_description(self):
        return self.description[:20]

    def get_image_url(self, suffix=None):
        if not suffix:
            return self.photo.url
        else:
            return self.photo.url + suffix

    def to_article(self):
        article = {
            "title": self.title,
            "description": self.description,
            "picurl": self.get_image_url("!80"),
            "url": self.smart_link
        }
        return article

    def update_rules(self, keywords_id):
        rules_origin = self.rules.all()
        for rule in rules_origin:
            self.rules.remove(rule.id)

        for keyword in keywords_id:
            self.rules.add(keyword)

    def save(self, force_insert=False, force_update=False, using=None):
        if self.html:
            try:
                self.html = BasicFormatter.format(self.html)
            except:
                pass
        super(RichText, self).save(force_insert, force_update, using)

    def to_json_response(self):
        return {
            "title": self.title,
            "description": self.description,
            "picture": self.get_image_url("!80"),
            "link": self.smart_link,
            "priority": self.priority,
        }