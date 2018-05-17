# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.six import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _

from apps.account.models import User
from common.model_fields import ListField
from common.models import CreateUpdateDeleteDateTimeModel, AddressModel, CreateUpdateDateTimeModel
from common.validators import sequence_validators


@python_2_unicode_compatible
class Hospital(CreateUpdateDeleteDateTimeModel, AddressModel):
    """医院信息表"""
    # 医院类别 公立（G）
    # 医院分级 一级 二级 三级
    # 医院等级 特等（T，针对三级） 甲等（A） 乙等(B) 丙等(C)
    GRADE_CHOICES = (('9-G3T', '公立三特'), ('8-G3A', '公立三甲'), ('7-G3B', '公立三乙'), ('6-G3C', '公立三丙'),
                     ('5-G2A', '公立二甲'), ('4-G2B', '公立二乙'), ('3-G2C', '公立二丙'),
                     ('2-G1A', '公立一甲'), ('1-G1B', '公立一乙'), ('0-G1C', '公立一丙'))

    name = models.CharField(_('医院名'), max_length=100, help_text=_('医院名'), db_index=True)
    grade = models.CharField(_('医院等级'), max_length=20, blank=True,
                             help_text=_('医院等级'), choices=GRADE_CHOICES)
    icon_pic = models.CharField('图标', blank=True, null=True, default='', help_text='医院图标', max_length=500)
    sequence = models.SmallIntegerField(_('排序号'), default=0,
                                        validators=sequence_validators(),
                                        help_text=_('序号越大排越前，范围为-999~999'))

    class Meta(AddressModel.Meta):
        db_table = 'hospital'
        verbose_name = '医院'
        verbose_name_plural = '医院'
        ordering = ('-id',)

    def __str__(self):
        return self.name



@python_2_unicode_compatible
class SetMeal(CreateUpdateDateTimeModel):
    """套餐/分类
    """
    hospital = models.ForeignKey(Hospital, blank=False,
                                       verbose_name='询价套餐关联医院', help_text='询价套餐关联医院',
                                       related_name='set_meals')
    name = models.CharField(verbose_name='套餐名', max_length=30, db_index=True,
                            help_text='套餐名', blank=False)
    description = models.TextField(verbose_name='描述', blank=True, default='', help_text='描述', max_length=1000)
    items = ListField(verbose_name='套餐项目', blank=False)
    present_price = models.DecimalField(verbose_name='当前价格', help_text='当前价格',
                                        decimal_places=2, null=False, max_digits=19)
    old_price = models.DecimalField(verbose_name='上次价格', max_digits=19, null=True,
                                     decimal_places=2, help_text='上次价格', editable=False)
    price_update_at = models.DateTimeField(verbose_name='套餐价格更新时间', help_text='套餐价格更新时间', blank=None, null=True, editable=False)
    sequence = models.SmallIntegerField(verbose_name='排序号', default=0,
                                        validators=sequence_validators(),
                                        help_text='序号越大排越前，范围为-999~999')
    author = models.ForeignKey(User, blank=False, verbose_name='套餐编辑者', help_text='套餐编辑者', related_name='set_meals')

    class Meta:
        db_table = 'set_meal'
        verbose_name = '套餐'
        verbose_name_plural = '套餐'
        ordering = ('-id',)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Item(CreateUpdateDateTimeModel):
    """体检项目"""
    hospital = models.ForeignKey(Hospital, verbose_name='项目关联医院', help_text='项目关联医院',
                                  related_name='items', blank=False)
    name = models.CharField(verbose_name='项目名', max_length=100, blank=False,
                            help_text='项目', db_index=True)
    content = models.TextField(verbose_name='项目内容', max_length=500, help_text=r"单个体检内容请以'/'分隔")

    item_category = models.CharField(verbose_name='项目大类', max_length=50, blank=True)
    description = models.CharField(verbose_name='项目意义', max_length=1000,
                                   blank=True, null=True, help_text='描述')
    present_price = models.DecimalField(verbose_name='当前价格', help_text='当前价格',
                                        decimal_places=2, null=False, max_digits=8)
    old_price = models.DecimalField(verbose_name='上次价格', max_digits=8, null=True,
                                     decimal_places=2, help_text='上次价格', editable=False)
    price_update_at = models.DateTimeField(verbose_name='项目价格更新时间', help_text='项目价格更新时间', blank=True, null=True, editable=False)

    class Meta:
        db_table = 'item'
        verbose_name = '项目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class ItemCategory(CreateUpdateDateTimeModel):
    """项目大类"""
    name = models.CharField(verbose_name='项目大类名', max_length=100, blank=False,
                            help_text='项目大类名')

    class Meta:
        db_table = 'item_category'
        verbose_name = '项目种类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
