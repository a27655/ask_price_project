# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.db.models import Q
from rest_framework import serializers
from rest_framework.viewsets import GenericViewSet

from apps.hospital.models import Hospital, Item, SetMeal
from rest_framework import mixins
from rest_framework import renderers
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from common.pagination import LargeResultsSetPagination
from common.permissions import IsSalesmanUser
from apps.hospital.serializers.weapp_serializers import HospitalListSerializers, HospitalItemsSerializers, \
    HospitalSetMealsSerializers, SetMealSerializers, items_classification
from apps.hospital.serializers.manage_serializers import SetMealUpdateSerializers


class HospitalsViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = (IsSalesmanUser,)
    pagination_class = LargeResultsSetPagination

    def get_serializer_class(self):
        if self.action == 'items':
            return HospitalItemsSerializers
        elif self.action == 'set_meals':
            return HospitalSetMealsSerializers
        elif self.action == 'set_meals_add':
            return SetMealUpdateSerializers
        else:
            return HospitalListSerializers

    def get_queryset(self):
        if self.action == 'items':
            queryset = Item.objects.filter(hospital=self.kwargs.get('pk')).order_by('-id')
            return queryset
        elif self.action == 'set_meals':
            queryset = SetMeal.objects.filter(hospital=self.kwargs.get('pk')).order_by('-id')
            return queryset
        else:
            province = self.request.region.province
            city = self.request.region.city
            queryset = Hospital.objects.filter(Q(province__icontains=province) & Q(city__icontains=city))
            queryset = self.serializer_class.setup_eager_loading(queryset)
            return queryset

    def hospital_exist(self):
        # 验证医院是否存在
        hospital = Hospital.objects.filter(id=self.kwargs.get('pk')).first()
        if not hospital:
            data = {'errors': '医院不存在'}
            return [False, Response(data, status=status.HTTP_400_BAD_REQUEST)]
        else:
            return [True, '']

    def list(self, request, *args, **kwargs):
        """
        weapp医院列表
        """
        self.serializer_class = self.get_serializer_class()
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, *args, **kwargs):
        """
        weapp医院详情
        """
        is_exist = self.hospital_exist()
        if not is_exist[0]:
            return is_exist[1]
        self.serializer_class = self.get_serializer_class()
        queryset = self.get_queryset()
        hospital = get_object_or_404(queryset, pk=kwargs.get('pk'))
        serializer = self.serializer_class(hospital, context={'request': request})
        return Response(serializer.data)

    @detail_route(url_path='items', methods=['get'])
    def items(self, request, pk):
        """
        weapp医院项目列表
        """
        is_exist = self.hospital_exist()
        if not is_exist[0]:
            return is_exist[1]
        self.serializer_class = self.get_serializer_class()
        queryset = self.get_queryset()
        items_classification_list = items_classification(queryset, self.request)
        return Response(items_classification_list)

    @detail_route(url_path='set-meals', methods=['get'])
    def set_meals(self, request, pk):
        """
        weapp医院套餐列表
        """
        is_exist = self.hospital_exist()
        if not is_exist[0]:
            return is_exist[1]
        self.serializer_class = self.get_serializer_class()
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.serializer_class(page, many=True, context={'request': request})
            return self.get_paginated_response(serializer.data)
        serializer = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(serializer.data)

    @detail_route(url_path='set-meals/add', methods=['post'])
    def set_meals_add(self, request, pk):
        """
        医院套餐创建
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
        is_exist = self.hospital_exist()
        if not is_exist[0]:
            return is_exist[1]
        self.serializer_class = self.get_serializer_class()
        serializer = self.serializer_class(data=request.data, context={'request': request, 'hospital_id':pk})
        serializer.is_valid(raise_exception=True)
        isinstance = serializer.save()
        serializer = SetMealSerializers(isinstance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SetMealViewSet(mixins.RetrieveModelMixin, GenericViewSet):
    permission_classes = (IsSalesmanUser,)

    def retrieve(self, request, *args, **kwargs):
        """
        weapp套餐详情
        """
        serializer_class = SetMealSerializers
        try:
            set_meal = SetMeal.objects.get(pk=kwargs.get('pk'))
        except Exception:
            data = {'errors': '套餐不存在'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializer_class(set_meal, context={'request': request})
        return Response(serializer.data)

    @detail_route(url_path='edit', methods=['post'])
    def set_meals_update(self, request, pk):
        """
        weapp套餐编辑
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
        user = request.user
        try:
            set_meal = SetMeal.objects.get(pk=pk)
        except Exception:
            data = {'errors': '套餐不存在'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        if user != set_meal.author:
            data = {'errors': '你没有修改此套餐的权限'}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        serializer = serializer_class(set_meal, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        set_mial = SetMeal.objects.filter(id=pk).first()
        serializer = SetMealSerializers(set_mial, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


