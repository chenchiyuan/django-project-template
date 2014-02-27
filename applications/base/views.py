# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.core.files.base import ContentFile
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from libs.hashs import md5
from libs.http import json_response
from libs.images import detect_image_type
from libs.models.storages import UpyunStorage


class ImageReceiverView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super(ImageReceiverView, self).dispatch(request, *args, **kwargs)

    def post(self, requests, *args, **kwargs):
        storage = UpyunStorage()
        memory_file = requests.FILES['file']
        image_name = memory_file.name
        image_size = memory_file.size
        data = memory_file.read()
        image_type = detect_image_type(data)
        file_name = md5(data) + ".%s" % image_type

        storage.save(file_name, ContentFile(data))
        url = storage.url(file_name) + "!hertz"
        context = {
            "success": 200,
            "name": image_name,
            "size": image_size,
            "url": url,
        }

        return json_response(context)