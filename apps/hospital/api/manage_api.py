# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import requests
import json
import logging

from django.db import transaction
from django.utils.encoding import uri_to_iri

from ask_price.settings import base
from django.db.models import Q
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from common.permissions import IsSalesmanUser, IsOperationUser
from common.pagination import StandardResultsSetPagination
from apps.hospital.models import Hospital, SetMeal, Item, ItemCategory
from apps.hospital.serializers.manage_serializers import HospitalListSerializers, HospitalItemsListSerializers, \
     HospitalSetMealListSerializers, SetMealSerializers, SetMealUpdateSerializers, ItemsBulkImportSerializers


logger = logging.getLogger(__name__)


class HospitalsListViewSet(viewsets.ReadOnlyModelViewSet):
    """
        医院列表

        ---
        list:
            parameters:
                - name: search
                  description: 搜索医院名，省，城市，模糊匹配
                  paramType: query
                  type: string
                
    """
    serializer_class = HospitalListSerializers
    permission_classes = (IsOperationUser, )
    pagination_class = StandardResultsSetPagination
    queryset = Hospital.objects.all().order_by('-id')
    search_fields = ('name', 'province', 'city')


    def filter_queryset(self, queryset):
        for backend in list(self.filter_backends):
            queryset = backend().filter_queryset(self.request, queryset, self)
        queryset = self.serializer_class.setup_eager_loading(queryset)
        return queryset


class HospitalDetailViewSet(APIView):
    """医院详情"""
    serializer_class = HospitalListSerializers
    permission_classes = (IsOperationUser,)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('hospital_id')
        hospital = Hospital.objects.filter(id=pk).first()
        if hospital:
            serializer = self.serializer_class(hospital, context={'request': request})
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            data = {'errors': ['医院不存在']}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)



class HospitalItemsListViewSet(viewsets.ModelViewSet):

    serializer_class = HospitalItemsListSerializers
    permission_classes = (IsOperationUser,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('name',)


    def get_queryset(self):
        hospital_id = self.kwargs.get('hospital_id')
        hospital = Hospital.objects.filter(id=hospital_id).prefetch_related('items').first()
        queryset = hospital.items.all().order_by('-id')
        queryset = self.serializer_class.setup_eager_loading(queryset)
        return queryset

    def list(self, request, *args, **kwargs):
        """医院项目列表
        ---
        parameters:
            - name: search
              description: 搜索项目名
              paramType: query
              type: string
        """
        hospital_id = self.kwargs.get('hospital_id')
        try:
            Hospital.objects.get(id=hospital_id)
        except Exception:
            data = {'errors': ['医院不存在']}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


    def create(self, request, *args, **kwargs):
        """创建医院项目
            ---
            parameters:
                - name: name
                  description: 套餐名
                  required: true
                  type: string
                - name: content
                  description: 项目内容
                  required: true
                  type: string
                - name: item_category
                  description: 项目大类
                  required: false
                  type: string
                - name: description
                  description: 项目意义
                  required: false
                  type: string
                - name: present_price
                  description: 价格
                  required: true
                  type: float 
        """
        hospital_id = kwargs.get('hospital_id')
        serializer = self.serializer_class(data=request.data, context={'request': request, 'hospital_id': hospital_id})
        serializer.is_valid(raise_exception=True)
        item_category = serializer.validated_data.get('item_category')
        if item_category:
            ItemCategory.objects.get_or_create(name=item_category)
        serializer.save(hospital_id=hospital_id)
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)


class ItemDetailViewSet(APIView):
    """项目详情"""
    serializer_class = HospitalItemsListSerializers
    permission_classes = (IsOperationUser,)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('item_id')
        item = Item.objects.filter(id=pk).first()
        if item:
            serializers = self.serializer_class(item, context={'request': request})
            return Response(data=serializers.data, status=status.HTTP_200_OK)
        else:
            data = {'errors':['单项不存在']}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, *args, **kwargs):

        """项目编辑
            ---
            parameters:
                - name: name
                  description: 套餐名
                  required: true
                  type: string
                - name: content
                  description: 项目内容
                  required: true
                  type: string
                - name: item_category
                  description: 项目大类
                  required: false
                  type: string
                - name: description
                  description: 项目意义
                  required: false
                  type: string
                - name: present_price
                  description: 价格
                  required: true
                  type: float
        """
        pk = kwargs.get('item_id')
        item = Item.objects.filter(id=pk).first()
        if item:
            serializers = self.serializer_class(item, data=request.data, context={'request': request})
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(serializers.data, status=status.HTTP_200_OK)
        else:
            data = {'errors': ['单项不存在']}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)



class HospitalSetMialsListViewSet(viewsets.ModelViewSet):
    """
        医院套餐列表

        ---
        list:
            parameters:
                - name: search
                  description: 搜索套餐
                  paramType: query
                  type: string

    """

    serializer_class = HospitalSetMealListSerializers
    permission_classes = (IsOperationUser,)
    pagination_class = StandardResultsSetPagination
    search_fields = ('name',)

    def get_queryset(self):
        hospital_id = self.kwargs.get('hospital_id')
        hospital = Hospital.objects.filter(id=hospital_id).prefetch_related('set_meals').first()
        queryset = hospital.set_meals.all().order_by('-id')
        queryset = self.serializer_class.setup_eager_loading(queryset)
        return queryset

    def list(self, request, *args, **kwargs):
        hospital_id = self.kwargs.get('hospital_id')
        try:
            Hospital.objects.get(id=hospital_id)
        except Exception:
            data = {'errors': ['医院不存在']}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class SetMialDetailViewSet(APIView):
    permission_classes = (IsOperationUser,)

    def get(self, request, *args, **kwargs):
        """套餐详情"""
        serializer_class = SetMealSerializers
        pk = kwargs.get('set_meals_id')
        set_mial = SetMeal.objects.filter(id=pk).first()
        if set_mial:
            serializers = serializer_class(set_mial, context={'request': request})
            return Response(data=serializers.data, status=status.HTTP_200_OK)
        else:
            data = {'errors': ['套餐不存在']}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


    def post(self, request, *args, **kwargs):
        """套餐编辑
        ---
        parameters:
            - name: name
              description: 套餐名
              required: true
              type: string
            - name: items
              description: 项目id列表
              required: true
              type: list  
        """
        serializer_class = SetMealUpdateSerializers
        pk = kwargs.get('set_meals_id')
        set_mial = SetMeal.objects.filter(id=pk).first()
        if not set_mial:
            data = {'errors': ['套餐不存在']}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializer_class(set_mial, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        set_mial = SetMeal.objects.filter(id=pk).first()
        serializer = SetMealSerializers(set_mial, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


class HospitalsSyncViewSet(APIView):
    permission_classes = (IsOperationUser,)

    @transaction.atomic
    def get(self, request, *args, **kwargs):
        """同步医院数据库"""
        logger.info('---------同步慧康達医院数据开始---------')
        try:
            response = requests.request('GET', base.HEALTHY_DOC_BASE_URL + '/api/kkk/')
        except Exception:
            data = {'errors': ['请求慧康達数据出错，请重试']}
            logger.info('---------请求慧康達数据出错, 同步医院数据失败--------')
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
        if response.status_code == 200:
            data = json.loads(response.content)
            for item in data:
                try:
                    Hospital.objects.update_or_create(name=item['name'], defaults=item)
                except Exception as e:
                    data = {'errors': [e]}
                    return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            logger.info('---------同步慧康達医院数据完成---------')
            return Response(status.HTTP_204_NO_CONTENT)

        else:
            data = {'errors': ['请求慧康達数据出错，请重试']}
            logger.info('---------请求慧康達数据出错, 同步医院数据失败--------')
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)


class ItemsBulkImportViewSet(APIView):
    permission_classes = (IsOperationUser,)
    serializer_class = ItemsBulkImportSerializers
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        """批量导入医院项目
        ---
        parameters:
            - name: file
              description: 医院项目Excel
              required: true
              type: file  
        """
        file = request.FILES.get('file')
        if file:
            serializer = self.serializer_class(data=request.data)
            tag = serializer.is_valid(raise_exception=True)
            if tag == True:
                logger.info('---------批量导入项目开始---------')
                upadte_items = serializer.validated_data['file'].get('upadte_items')
                create_items = serializer.validated_data['file'].get('create_items')
                if upadte_items:
                    for item in upadte_items:
                        try:
                            item_queryset = item.get('item_queryset')
                            del item['item_queryset']
                            item_queryset.update(**item)  # 更新
                        except Exception as e:
                            data = {'errors': [e]}
                            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
                    logger.info('批量更新了项目{}个'.format(len(upadte_items)))
                if create_items:
                    Item.objects.bulk_create(create_items)
                    logger.info('批量创建项目了{}个'.format(len(create_items)))
                logger.info('---------批量导入项目完成---------'.format(len(create_items)))
                return Response(status.HTTP_204_NO_CONTENT)
        else:
            data = {'errors': ['未传入文件']}
            return Response(data=data, status=status.HTTP_400_BAD_REQUEST)





