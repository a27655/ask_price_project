# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0003_auto_20170920_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.CharField(help_text='\u63cf\u8ff0', max_length=100, null=True, verbose_name='\u9879\u76ee\u610f\u4e49', blank=True),
        ),
    ]
