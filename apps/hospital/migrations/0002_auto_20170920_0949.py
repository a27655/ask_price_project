# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hospital', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='price_update_at',
            field=models.DateTimeField(help_text='\u9879\u76ee\u4ef7\u683c\u66f4\u65b0\u65f6\u95f4', verbose_name='\u9879\u76ee\u4ef7\u683c\u66f4\u65b0\u65f6\u95f4', null=True, editable=False, blank=True),
        ),
    ]
