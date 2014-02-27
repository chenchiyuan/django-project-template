# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from DjangoUeditor.models import UEditorField as UEField

from south.modelsinspector import add_introspection_rules


class UeEditorField(UEField):
    pass

add_introspection_rules([], [r"^libs\.models\.fields\.UeEditorField"])