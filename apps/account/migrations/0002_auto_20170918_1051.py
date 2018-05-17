# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='activate_code',
            field=models.CharField(max_length=50, unique=True, null=True, verbose_name='\u9500\u552e\u8d26\u53f7\u6fc0\u6d3b\u7801', blank=True),
        ),
    ]
