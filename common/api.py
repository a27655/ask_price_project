# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response

from common.models import CnRegion
from common.serializers import RegionSerializer

class GetRegionCodeAndArea(generics.GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = RegionSerializer

    def post(self, request):
        """
        使用省和市数据来请求城市数据，包括城市行政代码和城市行政区列表

        ---
        responseMessages:
            - code: 200
              message: 成功
            - code: 400
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        province = serializer.validated_data['province']
        city = serializer.validated_data['city']
        if province in CnRegion.ZXS and province == city:
            merge_name = province
            ids = CnRegion.objects.filter(merger_name=merge_name, level=1).values_list('id', flat=True)
            try:
                cn_region = CnRegion.objects.get(short_name=province, level=0)
            except CnRegion.DoesNotExist:
                data = {'errors': ['城市不存在']}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            areas_qs = CnRegion.objects.filter(parent_id__in=ids).values_list('short_name', 'name')
        else:
            merge_name = '{},{}'.format(province, city)
            try:
                cn_region = CnRegion.objects.get(merger_name=merge_name, level=1)
            except CnRegion.DoesNotExist:
                data = {'errors': ['城市不存在']}
                return Response(data=data, status=status.HTTP_400_BAD_REQUEST)
            areas_qs = CnRegion.objects.filter(parent_id=cn_region.id).values_list('short_name', 'name')
        res = dict([['region_code', cn_region.region_code]])
        res['areas'] = dict(areas_qs)
        return Response(data=res, status=status.HTTP_200_OK)