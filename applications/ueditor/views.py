# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.conf import settings
import time
import random


class ImageUploadView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ImageUploadView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return HttpResponse("Success", content_type="Application/javascript")

    def post(self, request, *args, **kwargs):
        response = self.save_file(request.FILES['upfile'])
        return HttpResponse(response, content_type="Application/javascript")

    def save_file(self, file, path=''):
        filename = unicode(time.time()) + unicode(random.random()) + file._get_name()
        file_handler = open('%s/%s' % (settings.MEDIA_ROOT, (path + filename).encode("utf-8")), 'wb')
        for chunk in file.chunks():
            file_handler.write(chunk)
        file_handler.close()

        response = "{'url':'/media/"+filename+"','title':'"+filename+"','state':'SUCCESS'}"
        return response