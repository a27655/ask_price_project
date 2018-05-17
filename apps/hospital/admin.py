# -*- coding: utf-8 -*-
from django.contrib import admin

from apps.hospital.models import Hospital, SetMeal, Item, ItemCategory


admin.site.register(Hospital)
admin.site.register(Item)
admin.site.register(SetMeal)
admin.site.register(ItemCategory)



