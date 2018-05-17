# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20170927_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activate_code',
            field=models.CharField(null=True, editable=False, max_length=50, blank=True, unique=True, verbose_name='\u9500\u552e\u8d26\u53f7\u6fc0\u6d3b\u6807\u8bc6\u7801'),
        ),
    ]
