# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from django.views.generic import ListView
from rest_framework import mixins
from rest_framework.authtoken.models import Token
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework import status

from apps.account.models import User
from apps.account.serializers.manage_serializers import ManagerLoginSerializer, UserManageListSerializer
from common.pagination import StandardResultsSetPagination
from common.permissions import IsOperationUser


class ManagerLoginToken(APIView):
    permission_classes = ()
    serializer_class = ManagerLoginSerializer

    def post(self, request, *args, **kwargs):
        """
        后台运维登录

        ---
        serializer: ManagerLoginSerializer
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response(data={'token': token.key, 'username': user.username})


class ManagerUserManageViewSet(mixins.ListModelMixin, GenericViewSet):
    """
    ---
    list:
        parameters:
            - name: search
              description: 用户邮箱，模糊搜索
              paramType: query
              type: string
    """
    permission_classes = (IsOperationUser, )
    search_fields = ('email',)
    queryset = User.seller_objects.all().exclude(is_superuser=True)
    serializer_class = UserManageListSerializer
    pagination_class = StandardResultsSetPagination


    @detail_route(['POST'], url_path='staff-change')
    def staff_status_change(self, request, *args, **kwargs):
        """员工状态改变(禁用/启用)"""
        user = self.get_object()
        is_staff = request.data.get('is_staff')
        if is_staff is not None:
            user.is_staff = int(is_staff)
            user.save()
            return Response(data={'is_staff': user.is_staff})
        else:
            data = {'errors': ['参数为传入']}
            return Response(data, status=status.HTTP_400_BAD_REQUEST)

