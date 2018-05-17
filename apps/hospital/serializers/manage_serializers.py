# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import json
import re
from datetime import datetime
from decimal import Decimal

import xlrd
from django.db.models import Sum
from rest_framework import serializers
from rest_framework.reverse import reverse
from apps.hospital.models import Hospital, Item, SetMeal, ItemCategory

class HospitalListSerializers(serializers.HyperlinkedModelSerializer):
    url = serializers.SerializerMethodField()
    set_meals_url = serializers.SerializerMethodField(label='医院套餐列表', help_text='医院套餐列表')
    items_url = serializers.SerializerMethodField(label='医院单项列表', help_text='医院单项列表')
    item_count = serializers.SerializerMethodField(label='医院可用单项数', help_text='医院可用单项数', default=0)
    grade = serializers.SerializerMethodField(label='医院等级', help_text='医院等级')

    class Meta:
        model = Hospital
        fields = (
            'url',
            'set_meals_url',
            'items_url',
            'id',
            'name',
            'grade',
            'province',
            'city',
            'item_count'
        )

    @staticmethod
    def setup_eager_loading(queryset):
        return queryset.prefetch_related('set_meals', 'items')

    def get_url(self, obj):
        return reverse('manage_hospital_detail', request=self.context['request'], kwargs={'hospital_id': obj.id})

    def get_set_meals_url(self, obj):
        return reverse('manage_set_meals_list', request=self.context['request'], kwargs={'hospital_id': obj.id})

    def get_items_url(self, obj):
        return reverse('manage_items_list', request=self.context['request'], kwargs={'hospital_id': obj.id})

    def get_item_count(self, obj):
        return obj.items.count()

    def get_grade(self, obj):
        if obj.grade:
            return obj.get_grade_display()
        else:
            return ''


class HospitalItemsListSerializers(serializers.HyperlinkedModelSerializer):
    """医院单项详情"""
    url = serializers.SerializerMethodField()
    selected = serializers.SerializerMethodField(help_text='套餐已选', label='套餐已选') # 便于前端编辑套餐选择项目, 均设为Flase

    class Meta:
        model = Item
        fields = (
            'url',
            'id',
            'name',
            'content',
            'item_category',
            'description',
            'present_price',
            'selected'
        )

    @staticmethod
    def setup_eager_loading(queryset):
        return queryset.select_related('hospital')

    def get_url(self, obj):
        return reverse('manage_item_detail', request=self.context['request'], kwargs={'item_id': obj.id})

    def get_selected(self, obj):
        return False

    def validate_present_price(self, value):
        if value < 0:
            raise serializers.ValidationError('项目价格不能小于零')
        return value

    def validate_name(self, value):
        clean_value = clean_item_name(value)
        if self.instance: # 更新项目 验证是否重名
            hospital = self.instance.hospital
            hospital_items = hospital.items.all().filter(name=clean_value)
            if hospital_items.count() > 1 or (hospital_items.count() == 1 and self.instance not in hospital_items):
                raise serializers.ValidationError('此医院已存在{}单项'.format(clean_value))
            return clean_value
        else:  # 创建项目 验证是否重名
            hospital_id = self.context.get('hospital_id')
            try:
                hospital = Hospital.objects.get(id=hospital_id)
            except Exception:
                raise serializers.ValidationError('医院不存在')
            is_exists = hospital.items.filter(name=clean_value).exists()
            if is_exists:
                raise serializers.ValidationError('此医院已存在{}单项'.format(clean_value))
            return clean_value

    def validate_content(self, value):
        return clean_item_content(value)

    def update(self, instance, validated_data):
        name = validated_data.get('name')
        present_price = validated_data.get('present_price')
        content = validated_data.get('content')
        item_category = validated_data.get('item_category')
        description = validated_data.get('description')

        old_price = instance.present_price
        instance.name = name
        instance.content = content
        instance.present_price = present_price
        instance.old_price = old_price
        instance.price_update_at = datetime.now()
        if item_category:
            instance.item_category = item_category
            ItemCategory.objects.get_or_create(name=item_category)
        else:
            instance.item_category = ''
        instance.description = description
        instance.save()
        return instance

    # def create(self, validated_data, **kwargs):
    #     hospital_id = self.context.get('hospital_id')
    #     hospital = Hospital.objects.get(id=hospital_id)
    #     name = validated_data.get('name')
    #     present_price = validated_data.get('present_price')
    #     content = validated_data.get('content')
    #     item_category = validated_data.get('item_category')
    #     description = validated_data.get('description')
    #
    #     instance = Item()
    #     instance.hospital = hospital
    #     instance.name = name
    #     instance.content = content
    #     instance.present_price = present_price
    #     if item_category:
    #         instance.item_category = item_category
    #         ItemCategory.objects.get_or_create(name=item_category)
    #     instance.description = description
    #     instance.save()
    #     return instance


class HospitalSetMealListSerializers(serializers.HyperlinkedModelSerializer):
    details_url = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField(label='单项数', help_text='单项数')
    present_price = serializers.SerializerMethodField(label='当前价格', help_text='当前价格')
    class Meta:
        model = SetMeal
        fields = (
            'details_url',
            'id',
            'name',
            'present_price',
            'item_count'
        )

    @staticmethod
    def setup_eager_loading(queryset):
        return queryset.select_related('hospital')

    def get_details_url(self, obj):
        return reverse('manage_set_mial_detail', request=self.context['request'], kwargs={'set_meals_id': obj.id})

    def get_item_count(self, obj):
        return len(obj.items)

    def get_present_price(self, obj):
        items = Item.objects.filter(id__in=obj.items)
        items_price_sum = Item.objects.filter(id__in=items).aggregate(Sum('present_price'))['present_price__sum']
        if items_price_sum != obj.present_price:
            old_price = obj.present_price
            obj.present_price = items_price_sum
            obj.old_price = old_price
            obj.price_update_at = datetime.now()
            obj.save()
        return obj.present_price


class SetMealSerializers(serializers.HyperlinkedModelSerializer):
    """套餐详情"""
    url = serializers.SerializerMethodField()
    item_count = serializers.SerializerMethodField(label='单项数', help_text='单项数')
    items = serializers.SerializerMethodField(label='单项列表', help_text='单项列表')
    present_price = serializers.SerializerMethodField(label='当前价格', help_text='当前价格')
    class Meta:
        model = SetMeal
        fields = (
            'url',
            'id',
            'name',
            'present_price',
            'item_count',
            'items'
        )

    def get_url(self, obj):
        return reverse('manage_set_mial_detail', request=self.context['request'], kwargs={'set_meals_id': obj.id})

    def get_present_price(self, obj):
        items = Item.objects.filter(id__in=obj.items)
        items_price_sum = Item.objects.filter(id__in=items).aggregate(Sum('present_price'))['present_price__sum']
        if items_price_sum != obj.present_price:
            old_price = obj.present_price
            obj.present_price = items_price_sum
            obj.old_price = old_price
            obj.price_update_at = datetime.now()
            obj.save()
        return obj.present_price

    def get_item_count(self, obj):
        return len(obj.items)

    def get_items(self, obj):
        items = Item.objects.filter(id__in=obj.items)
        serializers = HospitalItemsListSerializers(items, many=True, context=self.context)
        return serializers.data


class SetMealUpdateSerializers(serializers.ModelSerializer):
    """套餐编辑与创建"""

    class Meta:
        model = SetMeal
        fields = (
            'name',
            'items'
        )

    def validate_items(self, value):
        # 验证item内各个列表项是否存在
        if self.instance:
            hospital_items = self.instance.hospital.items.all()
        else:
            hospital = Hospital.objects.filter(pk=self.context.get('hospital_id')).prefetch_related('items').first()
            hospital_items = hospital.items.all()
        try:
            item_list = json.loads(value)  # 项目id列表
        except ValueError:
            raise serializers.ValidationError('items格式不正确')
        if isinstance(item_list, list):
            if len(item_list) == 0:
                raise serializers.ValidationError('套餐项目不能为空')
            for item in item_list:
                try:
                    item_instance = Item.objects.get(id=item)
                except Exception:
                    raise serializers.ValidationError('id为{}的单项不存在'.format(item))
                if not hospital_items.filter(pk=item).exists():
                    raise serializers.ValidationError('id为{}的单项({})不属于该套餐所属的医院'.format(item, item_instance.name))
                if item_list.count(item) > 1:
                    raise serializers.ValidationError('套餐不能包含相同的项目, id为{}的单项({})出现两次'.format(item, item_instance.name))
            return item_list
        raise serializers.ValidationError('items格式不正确')

    def validate_name(self, value):
        # 更新套餐 验证是否重名
        if self.instance:
            hospital = self.instance.hospital
            hospital_set_meals = hospital.set_meals.all().filter(name=value)
            if hospital_set_meals.count() > 1 or (hospital_set_meals.count() == 1 and self.instance not in hospital_set_meals):
                raise serializers.ValidationError('此医院已存在{}套餐'.format(value))
            return value
        # 创建套餐 验证是否重名
        else:
            hospital_id = self.context.get('hospital_id')
            try:
                hospital = Hospital.objects.get(id=hospital_id)
            except Exception:
                raise serializers.ValidationError('医院不存在')
            is_exists = hospital.set_meals.filter(name=value).exists()
            if is_exists:
                raise serializers.ValidationError('此医院已存在{}套餐'.format(value))
            return value

    def update(self, instance, validated_data):
        name = validated_data.get('name')
        items = validated_data.get('items')
        if items:
            # 更新套餐当前价格与上次价格
            present_price = Item.objects.filter(id__in=items).aggregate(Sum('present_price'))['present_price__sum']
            old_price = instance.present_price
            instance.present_price = present_price
            instance.old_price = old_price
            instance.price_update_at = datetime.now()
            instance.items = items
        instance.name = name
        instance.save()
        return instance

    def create(self, validated_data):
        name = validated_data.get('name')
        items = validated_data.get('items')
        hospital_id = self.context.get('hospital_id')
        hospital = Hospital.objects.get(id=hospital_id)
        user = self.context.get('request').user
        set_meals = SetMeal()
        set_meals.name = name
        set_meals.items = items
        present_price = Item.objects.filter(id__in=items).aggregate(Sum('present_price'))['present_price__sum']
        set_meals.present_price = present_price
        set_meals.author = user
        set_meals.hospital = hospital
        set_meals.save()
        return set_meals


class ItemsBulkImportSerializers(serializers.Serializer):
    title_list = ('项目名称', '项目内容', '项目意义', '项目价格')
    file = serializers.FileField(label='项目导入文件', help_text='项目导入文件', max_length=100, allow_empty_file=False)

    class Meta:
        fields = (
            'file',
        )

    def validate_file(self, value):
        upadte_items = []
        create_items = []
        # 判断文件格式
        if value.name[-4:] != 'xlsx':
            raise serializers.ValidationError('请传.xlsx后缀的文件')
        xlrd.Book.encoding = 'utf-8'
        data = xlrd.open_workbook(file_contents=value.read())
        sheets = data.sheets()
        sheet_names = [name.encode('utf-8').strip()  for name in data.sheet_names()]
        # 验证每一张表
        for sheet in sheets:
            name_col = [name.encode('utf-8').strip() for name in sheet.col_values(0)]  # 项目名称列
            nrows = sheet.nrows # 行数
            clean_sheet_name = sheet.name.encode('utf-8').strip()
            if nrows < 2:
                raise serializers.ValidationError('{}表有错误,表内数据为空'.format(clean_sheet_name))
            hospital = Hospital.objects.filter(name=clean_sheet_name).first()
            # 验证医院是否存在
            if not hospital:
                raise serializers.ValidationError('{}表有错误,此医院不存在'.format(clean_sheet_name))
            # 验证医院是否与其他sheet的医院重复
            if sheet_names.count(clean_sheet_name) > 1:
                raise serializers.ValidationError('表名错误,存在两张{}表'.format(clean_sheet_name))
            sheet_title = sheet.row_values(0)
            # 验证表头顺序是否正确
            for index in xrange(len(self.title_list)):
                if self.title_list[index] != sheet_title[index]:
                    raise serializers.ValidationError('{}表有错误,第{}列应该为{}'.format(sheet.name, index + 1, self.title_list[index]))
            # 循环验证每一行的数据是否合法
            for row in xrange(nrows):
                if row == 0:
                    continue  # 第一行是表头跳过
                row_item = sheet.row_values(row)
                # 除'项目名称', '项目内容', '项目意义', '项目价格'四项外的额外数据传入的具体报错提醒
                if len(row_item) > 4:
                    illegal_data_list = row_item[4:]
                    for index in xrange(len(illegal_data_list)):
                        illegal_data = illegal_data_list[index]
                        if illegal_data != '':
                            raise serializers.ValidationError(
                                "{}表有错误, 第{}行第{}列传入了非法数据".format(clean_sheet_name, row + 1, index + 5))

                present_price = row_item[3]
                clean_name, clean_content, clean_description = [i.encode('utf-8').strip() for i in row_item[0:3]]
                # 过滤项目内容
                clean_content = clean_item_content(clean_content)
                #过滤项目名称
                clean_name = clean_item_name(clean_name)
                # 判断项目名称和项目内容是否为空
                if not clean_name:
                    raise serializers.ValidationError('{}表有错误,第{}行{}为空'.format(sheet.name, row + 1, '项目名称'))
                if not clean_content:
                    raise serializers.ValidationError('{}表有错误,第{}行{}为空'.format(sheet.name, row + 1, '项目内容'))

                # 判断项目名称是否重复
                if name_col.count(clean_name) > 1:
                    raise serializers.ValidationError(
                        '{}表有错误, 第{}行{}与表内其他项目重复'.format(sheet.name, row + 1, '项目名称'))
                # 判断项目价格是否合法
                if not str(present_price).encode('utf-8').strip():
                    raise serializers.ValidationError(
                        '{}表有错误,第{}行项目价格为空'.format(sheet.name, row + 1))
                try:
                    clean_present_price = Decimal(present_price).quantize(Decimal('0.00'))
                except Exception:
                    raise serializers.ValidationError(
                        '{}表有错误,第{}行{}请填入数字'.format(sheet.name, row + 1, '项目价格'))
                if clean_present_price < 0:
                    raise serializers.ValidationError(
                        '{}表有错误,第{}行{}请不能小于零'.format(sheet.name, row + 1, '项目价格'))
                if clean_present_price >= 10**6:
                    raise serializers.ValidationError(
                        '{}表有错误,第{}行{}数额不能大于1000000'.format(sheet.name, row + 1, '项目价格'))

                # 生成可用数据
                item_queryset = Item.objects.filter(name=clean_name, hospital=hospital)
                item_instance = item_queryset.first()
                if item_instance and item_instance.present_price != clean_present_price:
                    update_dict = {
                             'item_queryset': item_queryset,  # 只包含一个实例的queryset
                             'content': clean_content,
                             'description': clean_description,
                             'present_price': clean_present_price,
                             'old_price': item_instance.present_price,
                             'price_update_at': datetime.now()
                    }
                    upadte_items.append(update_dict)
                elif item_instance and item_instance.present_price == clean_present_price:
                    update_dict = {
                        'item_queryset': item_queryset,  # 只包含一个实例的queryset
                        'content': clean_content,
                        'description': clean_description
                    }
                    upadte_items.append(update_dict)
                else:
                    item_instance = Item(hospital=hospital, name=clean_name, content=clean_content, description=clean_description, present_price=clean_present_price)
                    create_items.append(item_instance)
        return {'upadte_items':upadte_items, 'create_items':create_items}


# 过滤项目内容输入
def clean_item_content(value):
    sign_list = ['。', '，', '；', '：', '、', '.', ',', ';', ':', '&', '\\', ' ']
    for sign in sign_list:
        value = str(value).replace(sign, '/')
    re_rule = re.compile(r'/+')
    clean_list = re_rule.split(value)
    for i in xrange(clean_list.count('')):
        clean_list.remove('')
    clean_value = '/'.join(clean_list)
    return clean_value

# 过滤项目名称输入
def clean_item_name(value):
    replace_num = str(value).count(' ')
    clean_value = str(value).replace(' ', '', replace_num)
    return clean_value