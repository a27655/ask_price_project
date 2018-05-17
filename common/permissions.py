# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import unicode_literals

import logging

from rest_framework.permissions import BasePermission
from apps.account.models import User

logger = logging.getLogger(__name__)


class IsSalesmanUser(BasePermission):
    """销售账号权限"""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated() and request.user.user_type == User.SALESMAN_USER \
               and request.user.is_staff and request.user.is_active


class IsOperationUser(BasePermission):
    """运维账号权限"""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated() and request.user.user_type == User.OPERATION_USER \
               and request.user.is_staff and request.user.is_active
