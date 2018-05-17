# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0008_auto_20171020_1535'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='icon_pic',
            field=models.CharField(default='', max_length=500, blank=True, help_text='\u533b\u9662\u56fe\u6807', null=True, verbose_name='\u56fe\u6807'),
        ),
    ]
