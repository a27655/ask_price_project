# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from datetime import datetime

from django.db import models
from audit_log.models.managers import AuditLog
from django.utils.translation import ugettext_lazy as _
from django.utils.six import python_2_unicode_compatible


class CreateDateTimeModel(models.Model):
    """包含created_at字段的抽象类"""

    created_at = models.DateTimeField('创建时间', auto_now_add=True,
                                      help_text=_('创建时间'))

    class Meta:
        abstract = True


class UpdateDateTimeModel(models.Model):
    """包含updated_at字段的抽象类"""

    updated_at = models.DateTimeField('更新时间', auto_now=True,
                                      help_text=_('更新时间'))

    class Meta:
        abstract = True


class DeleteDateTimeModel(models.Model):
    """包含deleted_at字段的抽象类"""

    deleted_at = models.DateTimeField('删除时间', null=True, blank=True,
                                      help_text=_('删除时间'))

    class Meta:
        abstract = True

    def update_delete(self):
        '''更新为已删除'''
        if self.deleted_at:
            # 已删除
            re = 2
        else:
            # 更新为删除
            self.deleted_at = datetime.now()
            self.save(update_fields=['deleted_at'])
            re = 1
        return re


class CreateUpdateDateTimeModel(CreateDateTimeModel, UpdateDateTimeModel):
    """包含created_at updated_at两个字段的抽象类"""

    class Meta:
        abstract = True


class CreateUpdateDeleteDateTimeModel(CreateUpdateDateTimeModel,
                                      DeleteDateTimeModel):
    """包含created_at updated_at deleted_at三个字段的抽象类"""

    class Meta:
        abstract = True


class UpdateDeleteDateTimeModel(UpdateDateTimeModel, DeleteDateTimeModel):
    """包含updated_at deleted_at两个字段的抽象类"""

    class Meta:
        abstract = True


class DefaultManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        queryset = super(DefaultManager, self).get_queryset().filter(is_delete=False)
        return queryset


class DeleteFieldModel(models.Model):
    is_delete = models.BooleanField('删除', default=False, editable=False)

    objects = DefaultManager()
    audit_log = AuditLog()

    def soft_delete(self):
        self.is_delete = True
        self.updated_at = datetime.now()
        self.save(update_fields=['is_delete', 'updated_at'], force_update=True)

    class Meta:
        abstract = True



class AddressModel(models.Model):
    ZXS = ['北京', '上海', '天津', '重庆', '香港', '澳门', '台湾']

    region = models.CharField('地区', max_length=200, default='')
    province = models.CharField('省/直辖市/自治区', max_length=100, db_index=True, default='', blank=True)
    city = models.CharField('市', max_length=100, db_index=True, default='', blank=True)
    area = models.CharField('区/县', max_length=100, db_index=True, default='', blank=True)
    address = models.CharField(_('详细地址'), max_length=300, help_text=_('地址'), blank=True, default='')
    latitude = models.CharField(_('纬度'), max_length=50, blank=True,
                                help_text=_('纬度'), default='')
    longitude = models.CharField(_('经度'), max_length=50, blank=True,
                                 help_text=_('经度'), default='')
    zip_code = models.CharField(_('邮编'), help_text=_('邮编'), max_length=10,
                                blank=True, default='', db_index=True)

    class Meta:
        abstract = True
        index_together = ['province', 'city']

    @property
    def full_address(self):
        """完整详细地址"""
        return '{}{}{}{}'.format(self.province, self.city, self.area, self.address)

    @property
    def coordinate(self):
        """经纬度"""
        coordinate = '%s,%s' % (self.latitude, self.longitude)
        return coordinate

    def save(self, *args, **kwargs):
        if self.province in self.ZXS and self.province != self.city:
            self.area = self.city
            self.city = self.province
            self.province = ''
        self.region = '{} {} {}'.format(self.province, self.city, self.area)
        super(AddressModel, self).save(*args, **kwargs)


class CnRegionManager(models.Manager):
    def get_queryset(self):
        return super(CnRegionManager, self).get_queryset().exclude(name='市辖区')


@python_2_unicode_compatible
class CnRegion(models.Model):
    """全国行政区数据"""

    ZXS = ['北京', '上海', '天津', '重庆', '香港', '澳门', '台湾']
    LEVEL_CHOICES = ((0, '省/直辖市/自治区'),
                     (1, '市'),
                     (2, '区/县'))

    parent_id = models.PositiveIntegerField('父级ID', default='0')
    level = models.PositiveSmallIntegerField('层级', default='0')
    zip_code = models.CharField('邮政编码', max_length=6, default='000000')
    city_code = models.CharField('区号', max_length=4, default='')
    region_code = models.CharField('行政代码', max_length=20, default='0',
                                   db_index=True)
    name = models.CharField('名称', max_length=50, default='')
    short_name = models.CharField('简称', max_length=50, default='')
    merger_name = models.CharField('组合名', max_length=255, help_text='以英文逗号分隔',
                                   default='', db_index=True)
    picture = models.ImageField('背景图片', upload_to='cities/background', default='',
                                help_text='建议上传750*560的图片, 图片体积在1MB以内')
    pinyin = models.CharField('拼音', max_length=100, default='')
    ordering_time = models.DateTimeField('排序', default=None)
    is_hot = models.BooleanField(verbose_name='是否热门', default=False)
    is_able = models.BooleanField(verbose_name='是否启用', default=False)
    lng = models.DecimalField('经度', max_digits=12, decimal_places=8, default='0.000000')
    lat = models.DecimalField('纬度', max_digits=12, decimal_places=8, default='0.000000')
    objects = CnRegionManager()

    class Meta:
        verbose_name = '中国行政区'
        db_table = 'cn_region'
        verbose_name_plural = verbose_name
        permissions = (
        )

    def __str__(self):
        return self.merger_name