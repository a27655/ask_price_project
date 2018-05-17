# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

from rest_framework.pagination import PageNumberPagination


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 200
    page_size_query_param = 'page_size'
