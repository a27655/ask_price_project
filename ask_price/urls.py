# -*- coding: utf-8 -*-
"""ask_price URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from apps.account.api.manage_api import ManagerLoginToken, ManagerUserManageViewSet
from apps.account.api.weapp_api import WeappSellerLoginToken, WeappSellerRegister, UserResetPasswordAPI, \
    UserSendActiveEmail
from apps.account.views import UserActiveSuccessView, password_reset_confirm

from apps.hospital.api.manage_api import HospitalsListViewSet, HospitalDetailViewSet, HospitalItemsListViewSet, ItemDetailViewSet, \
     HospitalSetMialsListViewSet, SetMialDetailViewSet, HospitalsSyncViewSet, ItemsBulkImportViewSet
from apps.hospital.api.weapp_api import HospitalsViewSet as WeappHospitalViewSet
from apps.hospital.api.weapp_api import SetMealViewSet as WeappSetMealViewSet
from common.api import GetRegionCodeAndArea

if settings.DEBUG:
    router = DefaultRouter(schema_title='Pastebin API', schema_url='api')
else:
    router = SimpleRouter()

router.register(r'manage/users', ManagerUserManageViewSet,
                base_name='manager-users')

# router.register()
#
router.register(r'hospitals', WeappHospitalViewSet, base_name='hospital')
router.register(r'set-meals', WeappSetMealViewSet, base_name='set-meals')

manage_hospitals_list = HospitalsListViewSet.as_view({
    'get': 'list'
})

manage_items_list = HospitalItemsListViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

manage_set_meals_list = HospitalSetMialsListViewSet.as_view({
    'get': 'list'
})


urlpatterns = [
    url(r'^5811203/', include(admin.site.urls)),
    url(r'^5811203/doc/', include('django.contrib.admindocs.urls')),
    url(r'^api/', include(router.urls)),
    # url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/login/$', WeappSellerLoginToken.as_view(), name='weapp-login'),
    url(r'^api/register/$', WeappSellerRegister.as_view(), name='weapp-register'),
    url(r'^api/reset-password/$', UserResetPasswordAPI.as_view(), name='weapp-reset-password'),
    url(r'^api/send-active-email/$', UserSendActiveEmail.as_view(), name='send-active-email'),
    url(r'^api/manage/login/$', ManagerLoginToken.as_view(), name='manager-login'),

    url(r'^manage/account/activate/(?P<code>\w+)/$', UserActiveSuccessView.as_view(), name='user_activate'),
    # url(r'^password/change/$', 'django.contrib.auth.views.password_change', name="password_change"),
    # url(r'^password/change/done/$', 'django.contrib.auth.views.password_change_done', name="password_change_done"),
    url(r'^manage/password/reset/$', 'django.contrib.auth.views.password_reset', name="password_reset"),
    url(r'^manage/password/reset/done/$', 'django.contrib.auth.views.password_reset_done', name='password_reset_done'),
    url(r'^manage/password/reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', password_reset_confirm, name="password_reset_confirm"),
    url(r'^manage/password/done/$', 'django.contrib.auth.views.password_reset_complete', name="password_reset_complete")
]

urlpatterns += [
    # 管理后台医院
    url(r'^api/manage/hospitals/$', manage_hospitals_list, name='manage_hospitals_list'),
    url(r'^api/manage/hospitals/(?P<hospital_id>\d+)/$', HospitalDetailViewSet.as_view(), name='manage_hospital_detail'),
    # 管理后台套餐
    url(r'^api/manage/hospitals/(?P<hospital_id>\d+)/set-meals/$', manage_set_meals_list, name='manage_set_meals_list'),
    url(r'^api/manage/set-meals/(?P<set_meals_id>\d+)/$', SetMialDetailViewSet.as_view(), name='manage_set_mial_detail'),
    # 管理后台项目
    url(r'^api/manage/hospitals/(?P<hospital_id>\d+)/items/$', manage_items_list, name='manage_items_list'),
    url(r'^api/manage/items/(?P<item_id>\d+)/$', ItemDetailViewSet.as_view(), name='manage_item_detail'),
    # 城市信息
    url(r'^api/region/info/$', GetRegionCodeAndArea.as_view(), name='region-info'),
    # 同步慧康達医院数据
    url(r'^api/manage/hospitals/sync/$', HospitalsSyncViewSet.as_view(), name='manage_hospital_sync'),
    # 批量导入医院单项
    url(r'^api/manage/items/bulk_import/$', ItemsBulkImportViewSet.as_view(), name='manage_items_bulk_import')

]

# 接口文档
if settings.DEBUG:
    urlpatterns += [
        url(r'^docs/', include('rest_framework_swagger.urls')),
    ]

