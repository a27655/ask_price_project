# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0002_auto_20170920_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='setmeal',
            name='price_update_at',
            field=models.DateTimeField(help_text='\u5957\u9910\u4ef7\u683c\u66f4\u65b0\u65f6\u95f4', verbose_name='\u5957\u9910\u4ef7\u683c\u66f4\u65b0\u65f6\u95f4', null=True, editable=False, blank=None),
        ),
    ]
