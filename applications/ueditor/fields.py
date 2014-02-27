# -*- coding: utf-8 -*-
# __author__ = chenchiyuan

from __future__ import division, unicode_literals, print_function
from django.db.models import TextField
from widgets import UeditorWidget


class UEditorField(TextField):
    def formfield(self, **kwargs):
        kwargs['widget'] = UeditorWidget
        return super(UEditorField, self).formfield(**kwargs)


try:
    from south.modelsinspector import add_ignored_fields, add_introspection_rules
    add_introspection_rules([], [r"^applications.ueditor\.fields\.UEditorField"])
except:
    pass