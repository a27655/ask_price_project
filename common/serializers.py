# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals
from rest_framework import serializers


class RegionSerializer(serializers.Serializer):
    province = serializers.CharField(label='省/直辖市/自治区', help_text='省/直辖市/自治区')
    city = serializers.CharField(label='市', help_text='市')

    class Meta:
        fields = ('province', 'city')