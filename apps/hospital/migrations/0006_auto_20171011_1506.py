# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0005_auto_20170926_0912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setmeal',
            name='old_price',
            field=models.DecimalField(decimal_places=2, editable=False, max_digits=19, help_text='\u4e0a\u6b21\u4ef7\u683c', null=True, verbose_name='\u4e0a\u6b21\u4ef7\u683c'),
        ),
        migrations.AlterField(
            model_name='setmeal',
            name='present_price',
            field=models.DecimalField(help_text='\u5f53\u524d\u4ef7\u683c', verbose_name='\u5f53\u524d\u4ef7\u683c', max_digits=19, decimal_places=2),
        ),
    ]
