# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.contrib import admin
from django.db import models
from applications.weixin.widgets import ForeighUpyunImageWidget, UpyunImageWidget
from models import App, Rule, MenuItem, SubscribeItem, Photo, RichText


class MenuInline(admin.TabularInline):
    model = MenuItem

    raw_id_fields = ["rule"]


class SubscribeInline(admin.TabularInline):
    model = SubscribeItem
    raw_id_fields = ["rule"]

    max_num = 1


class PhotoAdmin(admin.ModelAdmin):
    readonly_fields = ["md5", ]
    list_display = ("id", "name", "md5", "thumbnail")

    formfield_overrides = {
        models.ImageField: {'widget': UpyunImageWidget},
    }

    search_fields = ["name", ]

    def thumbnail(self, obj):
        return '<a href="%s"> <img src="%s" width="50" height="50"> </a>' % (obj.url, obj.url)
    thumbnail.allow_tags = True
    thumbnail.short_description = u"缩略图"


class RichTextAdmin(admin.ModelAdmin):
    class Media:
        css = {
            "all": ("/static/css/admin-override.css", ),
        }

    filter_horizontal = ["rules"]
    search_fields = ["title", ]
    list_display = ["title", "list_rules", "link", "priority"]

    list_filter = (
        ("rules",)
    )

    def list_rules(self, obj):
        rules = obj.rules.all()
        return ",".join(map(lambda rule: rule.text, rules))
    list_rules.short_description = u"关键字"

    def formfield_for_foreignkey(self, db_field, request=None, **kwargs):
        db = kwargs.get('using')
        if db_field.name == "photo":
            kwargs['widget'] = ForeighUpyunImageWidget(db_field.rel, self.admin_site, using=db)

        response = super(RichTextAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
        return response


class RuleAdmin(admin.ModelAdmin):
    list_display = ("text", "count")

    search_fields = ["text", ]

    def count(self, obj):
        obj_count = obj.richtext_set.all().count()
        return '<a href="/admin/weixin/richtext/?rules__id__exact=%s">%d</a>' % (obj.id, obj_count)

    count.short_description = u"图文消息个数"
    count.allow_tags = True


class AppAdmin(admin.ModelAdmin):
    inlines = [
        SubscribeInline,
        MenuInline
    ]
    readonly_fields = ['app_url', 'app_token']


admin.site.register(App, AppAdmin)
admin.site.register(Rule, RuleAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(RichText, RichTextAdmin)