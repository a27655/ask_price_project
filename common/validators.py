# -*- coding: utf-8 -*-

from __future__ import absolute_import
from __future__ import unicode_literals

import re
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


def validate_mobile_phone(value):
    """验证手机号

    规则：全数字，首位为1，长度11
    """
    # 20170511 update
    phone_starter = [
        '134', '135', '136', '137', '138', '139', '147', '150', '151', '152', '157', '158', '159', '172', '178', '182',
        '183', '184', '187', '188', '130', '131', '132', '145', '155', '156', '171', '175', '176', '185', '186', '133',
        '149', '153', '173', '177', '180', '181', '189', '170'
    ]

    r = re.compile(r'^1\d{10}$')
    if not r.match(value) or not value[:3] in phone_starter :
        raise ValidationError('不合法的手机号', code='invalid')


def sequence_validators():
    """排序号验证器"""
    _min_limit = MinValueValidator(-999, '不能小于999')
    _max_limit = MaxValueValidator(999, '不能大于999')
    return [_min_limit, _max_limit]



def validate_sckj_email(value):
    pass


def settlement_ratio_validators():
    _min_limit = MinValueValidator(0.01, '结算比例不能低于0.01')
    _max_limit = MaxValueValidator(1, '结算比例不能高于1')
    return [_min_limit, _max_limit]

