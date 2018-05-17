# -*- coding: utf-8 -*-
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from apps.account.models import User

class MyUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('用户类型', {'fields': ('user_type',)}),
    )

admin.site.register(User, MyUserAdmin)
