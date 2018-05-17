# -*- coding: utf-8 -*-
from django.core.cache import cache


class Region(object):
    def __init__(self, province, city, region_code):
        self.province = province
        self.city = city
        self.region_code = region_code


class RegionMiddleware(object):
    """根据Header里的region_code查询对应的地区信息，存入request对象里"""

    def process_request(self, request):
        region_code = request.META.get('HTTP_REGION_CODE', '330100000000')
        region = get_region(region_code)
        request.region = region
        return None


def get_region(region_code):
    from common.models import CnRegion
    region = cache.get(region_code)
    if region:
        return region
    if not region_code:
        region = Region('浙江', '杭州', '330100000000')
    else:
        try:
            merger_name = CnRegion.objects.get(region_code=region_code).merger_name
        except CnRegion.DoesNotExist:
            region = Region('浙江', '杭州', '330100000000')
        else:
            if len(merger_name.split(',')) == 2:
                region = Region(*merger_name.split(','), region_code=region_code)
            elif len(merger_name.split(',')) == 1:
                region = Region(province='', city=merger_name, region_code=region_code)
            else:
                region = Region('浙江', '杭州', '330100000000')
    cache.set(region_code, region, 60 * 60 * 24 * 365)
    return region
