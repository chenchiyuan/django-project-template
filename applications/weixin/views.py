# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.http import HttpResponse, Http404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View, TemplateView
from applications.weixin.models import RichText
from applications.weixin.weixin.receiver import WeiXinReceiver


class WeiXinResponseView(View):
    def get(self, request, *args, **kwargs):
        receiver = WeiXinReceiver(request)
        return HttpResponse(receiver.echo())

    def post(self, request, *args, **kwargs):
        receiver = WeiXinReceiver(request)
        return HttpResponse(receiver.dispatch())

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(WeiXinResponseView, self).dispatch(request, *args, **kwargs)


class WeiXinDetailView(TemplateView):
    template_name = "text_detail.html"

    def get_context_data(self, **kwargs):
        rich_text = RichText.get_by_unique(**kwargs)
        if not rich_text:
            raise Http404("没有指定的图文消息")

        context = super(WeiXinDetailView, self).get_context_data(**kwargs)
        context['rich_text'] = rich_text
        return context