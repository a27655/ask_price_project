# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import apps.account.models
import django.contrib.auth.models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_auto_20170918_1051'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
                ('seller_objects', apps.account.models.SellerObjectsManager()),
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='activate_code',
            field=models.CharField(max_length=50, unique=True, null=True, verbose_name='\u9500\u552e\u8d26\u53f7\u6fc0\u6d3b\u6807\u8bc6\u7801', blank=True),
        ),
    ]
