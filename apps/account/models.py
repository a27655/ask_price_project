# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import string

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils.six import python_2_unicode_compatible

# Create your models here.


class SellerObjectsManager(UserManager):
    """销售人员"""
    def get_queryset(self):
        return super(SellerObjectsManager, self).get_queryset().filter(user_type=User.SALESMAN_USER,
                                                                       is_active=True)

    def create(self, email, password, **kwargs):
        """创建销售用户"""
        def get_random_code():
            code = "".join(random.sample(string.ascii_letters+string.digits, 20))
            is_exist = User.objects.filter(activate_code=code).exists()
            return is_exist and get_random_code() or code

        username = str(email).split('@', 1)[0]
        user = User(username=username, email=email, is_active=False, is_staff=True,
                    user_type=User.SALESMAN_USER, activate_code=get_random_code())
        user.set_password(password)
        user.save()
        return user


@python_2_unicode_compatible
class User(AbstractUser):
    """
    用户，继承自:model:`auth.AbstractUser`
    """
    SALESMAN_USER = 0
    OPERATION_USER = 1

    USER_TYPE_CHOICES = (
        (SALESMAN_USER, '销售人员'),
        (OPERATION_USER, '运维人员'),
    )
    user_type = models.PositiveSmallIntegerField(verbose_name='用户类型', choices=USER_TYPE_CHOICES, default=0)
    activate_code = models.CharField(verbose_name='销售账号激活标识码', max_length=50, null=True, blank=True, unique=True, editable=False)

    objects = UserManager()
    seller_objects = SellerObjectsManager()

    class Meta(AbstractUser.Meta):
        db_table = 'auth_user'
        verbose_name = '用户'
        verbose_name_plural = '用户'

    def __str__(self):
        if self.email:
            return self.email
        else:
            return self.username
