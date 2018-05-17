# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from datetime import datetime

from django.db.models import Sum
from rest_framework import serializers
from rest_framework.reverse import reverse
from apps.hospital.models import Hospital, Item, SetMeal

class HospitalListSerializers(serializers.HyperlinkedModelSerializer):
    greate_list = ('9-G3T', '8-G3A','7-G3B', '6-G3C', '5-G2A', '4-G2B', '3-G2C', '2-G1A', '1-G1B', '0-G1C')

    url = serializers.SerializerMethodField()
    set_meals_url = serializers.SerializerMethodField(label='医院套餐列表', help_text='医院套餐列表')
    grade = serializers.SerializerMethodField(label='医院等级', help_text='医院等级')
    full_address = serializers.SerializerMethodField(label='医院完整地址', help_text='医院完整地址')
    grade_index = serializers.SerializerMethodField(label='医院等级排序', help_text='医院等级排序')

    class Meta:
        model = Hospital
        fields = (
            'url',
            'set_meals_url',
            'id',
            'name',
            'grade',
            'full_address',
            'grade_index',
            'icon_pic'
        )

    @staticmethod
    def setup_eager_loading(queryset):
        return queryset.prefetch_related('set_meals', 'items')

    def get_url(self, obj):
        return reverse('hospital-detail', request=self.context['request'], kwargs={'pk': obj.id})

    def get_set_meals_url(self, obj):
        return reverse('hospital-set-meals', request=self.context['request'], kwargs={'pk': obj.id})

    def get_full_address(self, obj):
        return obj.full_address

    def get_grade(self, obj):
        if obj.grade and str(obj.grade) in self.greate_list:
            return obj.get_grade_display()
        else:
            return ''

    def get_grade_index(self, obj):
        if obj.grade:
            try:
                grade_num = int(obj.grade[0])
                return 10 - grade_num
            except Exception:
                return 11
        else: # 没有等级与等级错误返回 数字11
            return 11


class HospitalItemsSerializers(serializers.HyperlinkedModelSerializer):
    """医院单项"""
    checked = serializers.SerializerMethodField(label='选中', help_text='选中') # 小程序指定字段, 便于前端操作, 均设为Flase
    unfold = serializers.SerializerMethodField(label='展开', help_text='展开')  # 小程序指定字段, 便于前端操作, 均设为Flase
    class Meta:
        model = Item
        fields = (
            'id',
            'name',
            'content',
            'item_category',
            'description',
            'present_price',
            'old_price',
            'price_update_at',
            'checked',
            'unfold'
        )

    @staticmethod
    def setup_eager_loading(queryset):
        return queryset.select_related('hospital')

    def get_checked(self, obj):
        return False

    def get_unfold(self, obj):
        return False


class HospitalSetMealsSerializers(serializers.HyperlinkedModelSerializer):
    """医院套餐列表"""
    details_url = serializers.SerializerMethodField()
    edit_url = serializers.SerializerMethodField(label='编辑套餐url', help_text='编辑套餐url')
    item_count = serializers.SerializerMethodField(label='单项数', help_text='单项数')
    present_price = serializers.SerializerMethodField(label='当前价格', help_text='当前价格')
    price_update_at = serializers.SerializerMethodField(label='套餐价格更新时间', help_text='套餐价格更新时间')
    class Meta:
        model = SetMeal
        fields = (
            'details_url',
            'edit_url',
            'id',
            'name',
            'description',
            'present_price',
            'old_price',
            'price_update_at',
            'item_count',
        )

    @staticmethod
    def setup_eager_loading(queryset):
        return queryset.select_related('hospital')

    def get_details_url(self, obj):
        return reverse('set-meals-detail', request=self.context['request'], kwargs={'pk': obj.id})

    def get_edit_url(self, obj):
        return reverse('set-meals-edit', request=self.context['request'], kwargs={'pk': obj.id})

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
        return str(obj.present_price)

    def get_price_update_at(self, obj):
        # 如果有价格更新时间，返回价格更新时间；如果没有则返回创建时间
        if obj.price_update_at:
            return obj.price_update_at.strftime('%Y-%m-%d %H:%M:%S')
        else:
            return obj.created_at.strftime('%Y-%m-%d %H:%M:%S')



class SetMealSerializers(serializers.HyperlinkedModelSerializer):
    """套餐详情"""
    url = serializers.SerializerMethodField()
    edit_url = serializers.SerializerMethodField(label='编辑套餐url', help_text='编辑套餐url')
    item_count = serializers.SerializerMethodField(label='单项数', help_text='单项数')
    items = serializers.SerializerMethodField(label='单项列表', help_text='单项列表')
    present_price = serializers.SerializerMethodField(label='当前价格', help_text='当前价格')
    class Meta:
        model = SetMeal
        fields = (
            'url',
            'edit_url',
            'id',
            'name',
            'description',
            'present_price',
            'old_price',
            'item_count',
            'items'
        )

    def get_url(self, obj):
        return reverse('set-meals-detail', request=self.context['request'], kwargs={'pk': obj.id})

    def get_edit_url(self, obj):
        return reverse('set-meals-edit', request=self.context['request'], kwargs={'pk': obj.id})

    # 检查项目总价与套餐现价是否相等，相等则返回，不相等则更新
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
        # 将项目列表按项目大类分类
        items = Item.objects.filter(id__in=obj.items)
        items_classification_list = items_classification(items, self.context['request'])
        return items_classification_list


def items_classification(query_set, request):
    """项目列表按项目大类进行分类"""
    classify_dict = {
    }
    items_classify_list = []
    for item in query_set:
        if not item.item_category:
            if classify_dict.get('其他'):
                classify_dict['其他'].append(item)
            else:
                classify_dict['其他'] = []
                classify_dict['其他'].append(item)
            continue
        if classify_dict.get(item.item_category):
            classify_dict[item.item_category].append(item)
            continue
        else:
            classify_dict[item.item_category] = [item]
    keys = classify_dict.keys()
    for key in keys:
        serializers = HospitalItemsSerializers(classify_dict[key], many=True, context={'request': request})
        items_classify_list.append(dict(item_category=key, items=serializers.data))
    return items_classify_list


