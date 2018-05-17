# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0007_auto_20171011_1558'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='icon_pic',
            field=models.CharField(default='', help_text='\u533b\u9662\u56fe\u6807', max_length=500, verbose_name='\u56fe\u6807', blank=True),
        ),
    ]
