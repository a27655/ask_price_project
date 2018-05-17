# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0004_auto_20170921_1356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hospital',
            name='icon_pic',
            field=models.ImageField(default='', upload_to='hospital/icon', max_length=500, blank=True, help_text='\u5efa\u8bae\u4e0a\u4f20125*125\u7684\u56fe\u7247', verbose_name='\u56fe\u6807'),
        ),
    ]
