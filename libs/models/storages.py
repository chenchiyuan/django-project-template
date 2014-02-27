# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.conf import settings

image_url = lambda name: settings.IMG_HOST + name

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

from django.core.files.storage import Storage
from django.core.files.base import File

import upyun


class UpYunStorageFile(File):
    def __init__(self, name, mode, storage):
        self._name = name
        self._storage = storage
        self._mode = mode

    @property
    def size(self):
        if not hasattr(self, '_size'):
            self._size = self._storage.size(self._name)
        return self._size

    def read(self, num_bytes=None):
        return self._storage.read(self._name)

    def write(self, content):
        self._storage.save(self._name, content)

    def close(self):
        pass


class UpyunStorage(Storage):
    def __init__(self):
        self.upyun = upyun.UpYun(settings.UPYUN_BUCKET, settings.UPYUN_USER, settings.UPYUN_PASS,
                                 timeout=30, endpoint=upyun.ED_AUTO)

    def _open(self, name, mode='rb'):
        return UpYunStorageFile(name, mode, self)

    def save(self, name, content):
        if name is None:
            name = content.name

        return self._save(name, content)

    def _save(self, name, content):
        self._put_file(name, content.read())
        content.close()
        return name

    def read(self, name):
        return self._read(name)

    def _read(self, name):
        name = self._clean_name(name)
        content = self.upyun.get(name)
        return content

    def _put_file(self, name, content):
        name = self._clean_name(name)
        self.upyun.put(name, content, checksum=True)

    def _clean_name(self, name):
        if type(name) is unicode:
            return name.encode('utf-8')
        else:
            return name

    def exists(self, name):
        try:
            res = self.upyun.getinfo(name)
            return True
        except:
            return False

    def size(self, name):
        res = self.upyun.getinfo(name)
        return res['file-size']

    def url(self, name):
        return image_url(name)