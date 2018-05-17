# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import ast

from django.db import models
from common import validators



class MobilePhoneField(models.CharField):
    """手机号model字段"""

    default_validators = [validators.validate_mobile_phone]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 15)
        # if not args:
        #     args[0] = _('手机号')
        super(MobilePhoneField, self).__init__(*args, **kwargs)


class ListField(models.TextField):
    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return ''

        return unicode(value)  # use str(value) in Python 3

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)
