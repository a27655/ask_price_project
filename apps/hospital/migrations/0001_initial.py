# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import common.model_fields
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='\u521b\u5efa\u65f6\u95f4', verbose_name='\u521b\u5efa\u65f6\u95f4', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='\u66f4\u65b0\u65f6\u95f4', verbose_name='\u66f4\u65b0\u65f6\u95f4', auto_now=True)),
                ('deleted_at', models.DateTimeField(help_text='\u5220\u9664\u65f6\u95f4', null=True, verbose_name='\u5220\u9664\u65f6\u95f4', blank=True)),
                ('region', models.CharField(default='', max_length=200, verbose_name='\u5730\u533a')),
                ('province', models.CharField(default='', max_length=100, verbose_name='\u7701/\u76f4\u8f96\u5e02/\u81ea\u6cbb\u533a', db_index=True, blank=True)),
                ('city', models.CharField(default='', max_length=100, verbose_name='\u5e02', db_index=True, blank=True)),
                ('area', models.CharField(default='', max_length=100, verbose_name='\u533a/\u53bf', db_index=True, blank=True)),
                ('address', models.CharField(default='', help_text='\u5730\u5740', max_length=300, verbose_name='\u8be6\u7ec6\u5730\u5740', blank=True)),
                ('latitude', models.CharField(default='', help_text='\u7eac\u5ea6', max_length=50, verbose_name='\u7eac\u5ea6', blank=True)),
                ('longitude', models.CharField(default='', help_text='\u7ecf\u5ea6', max_length=50, verbose_name='\u7ecf\u5ea6', blank=True)),
                ('zip_code', models.CharField(default='', max_length=10, blank=True, help_text='\u90ae\u7f16', verbose_name='\u90ae\u7f16', db_index=True)),
                ('name', models.CharField(help_text='\u533b\u9662\u540d', max_length=100, verbose_name='\u533b\u9662\u540d', db_index=True)),
                ('grade', models.CharField(blank=True, help_text='\u533b\u9662\u7b49\u7ea7', max_length=20, verbose_name='\u533b\u9662\u7b49\u7ea7', choices=[('9-G3T', '\u516c\u7acb\u4e09\u7279'), ('8-G3A', '\u516c\u7acb\u4e09\u7532'), ('7-G3B', '\u516c\u7acb\u4e09\u4e59'), ('6-G3C', '\u516c\u7acb\u4e09\u4e19'), ('5-G2A', '\u516c\u7acb\u4e8c\u7532'), ('4-G2B', '\u516c\u7acb\u4e8c\u4e59'), ('3-G2C', '\u516c\u7acb\u4e8c\u4e19'), ('2-G1A', '\u516c\u7acb\u4e00\u7532'), ('1-G1B', '\u516c\u7acb\u4e00\u4e59'), ('0-G1C', '\u516c\u7acb\u4e00\u4e19')])),
                ('icon_pic', models.ImageField(default='', upload_to='hospital/icon', blank=True, help_text='\u5efa\u8bae\u4e0a\u4f20125*125\u7684\u56fe\u7247', verbose_name='\u56fe\u6807')),
                ('sequence', models.SmallIntegerField(default=0, help_text='\u5e8f\u53f7\u8d8a\u5927\u6392\u8d8a\u524d\uff0c\u8303\u56f4\u4e3a-999~999', verbose_name='\u6392\u5e8f\u53f7', validators=[django.core.validators.MinValueValidator(-999, '\u4e0d\u80fd\u5c0f\u4e8e999'), django.core.validators.MaxValueValidator(999, '\u4e0d\u80fd\u5927\u4e8e999')])),
            ],
            options={
                'ordering': ('-id',),
                'abstract': False,
                'verbose_name_plural': '\u533b\u9662',
                'db_table': 'hospital',
                'verbose_name': '\u533b\u9662',
            },
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='\u521b\u5efa\u65f6\u95f4', verbose_name='\u521b\u5efa\u65f6\u95f4', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='\u66f4\u65b0\u65f6\u95f4', verbose_name='\u66f4\u65b0\u65f6\u95f4', auto_now=True)),
                ('name', models.CharField(help_text='\u9879\u76ee', max_length=100, verbose_name='\u9879\u76ee\u540d', db_index=True)),
                ('content', models.TextField(help_text="\u5355\u4e2a\u4f53\u68c0\u5185\u5bb9\u8bf7\u4ee5'/'\u5206\u9694", max_length=500, verbose_name='\u9879\u76ee\u5185\u5bb9')),
                ('item_category', models.CharField(max_length=50, verbose_name='\u9879\u76ee\u5927\u7c7b', blank=True)),
                ('description', models.CharField(default='', help_text='\u63cf\u8ff0', max_length=100, verbose_name='\u9879\u76ee\u610f\u4e49', blank=True)),
                ('present_price', models.DecimalField(help_text='\u5f53\u524d\u4ef7\u683c', verbose_name='\u5f53\u524d\u4ef7\u683c', max_digits=8, decimal_places=2)),
                ('old_price', models.DecimalField(decimal_places=2, editable=False, max_digits=8, help_text='\u4e0a\u6b21\u4ef7\u683c', null=True, verbose_name='\u4e0a\u6b21\u4ef7\u683c')),
                ('price_update_at', models.DateTimeField(help_text='\u9879\u76ee\u4ef7\u683c\u66f4\u65b0\u65f6\u95f4', verbose_name='\u9879\u76ee\u4ef7\u683c\u66f4\u65b0\u65f6\u95f4', editable=False)),
                ('hospital', models.ForeignKey(related_name='items', verbose_name='\u9879\u76ee\u5173\u8054\u533b\u9662', to='hospital.Hospital', help_text='\u9879\u76ee\u5173\u8054\u533b\u9662')),
            ],
            options={
                'db_table': 'item',
                'verbose_name': '\u9879\u76ee',
                'verbose_name_plural': '\u9879\u76ee',
            },
        ),
        migrations.CreateModel(
            name='ItemCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='\u521b\u5efa\u65f6\u95f4', verbose_name='\u521b\u5efa\u65f6\u95f4', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='\u66f4\u65b0\u65f6\u95f4', verbose_name='\u66f4\u65b0\u65f6\u95f4', auto_now=True)),
                ('name', models.CharField(help_text='\u9879\u76ee\u5927\u7c7b\u540d', max_length=100, verbose_name='\u9879\u76ee\u5927\u7c7b\u540d')),
            ],
            options={
                'db_table': 'item_category',
                'verbose_name': '\u9879\u76ee\u79cd\u7c7b',
                'verbose_name_plural': '\u9879\u76ee\u79cd\u7c7b',
            },
        ),
        migrations.CreateModel(
            name='SetMeal',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(help_text='\u521b\u5efa\u65f6\u95f4', verbose_name='\u521b\u5efa\u65f6\u95f4', auto_now_add=True)),
                ('updated_at', models.DateTimeField(help_text='\u66f4\u65b0\u65f6\u95f4', verbose_name='\u66f4\u65b0\u65f6\u95f4', auto_now=True)),
                ('name', models.CharField(help_text='\u5957\u9910\u540d', max_length=30, verbose_name='\u5957\u9910\u540d', db_index=True)),
                ('description', models.TextField(default='', help_text='\u63cf\u8ff0', max_length=1000, verbose_name='\u63cf\u8ff0', blank=True)),
                ('items', common.model_fields.ListField(verbose_name='\u5957\u9910\u9879\u76ee')),
                ('present_price', models.DecimalField(help_text='\u5f53\u524d\u4ef7\u683c', verbose_name='\u5f53\u524d\u4ef7\u683c', max_digits=8, decimal_places=2)),
                ('old_price', models.DecimalField(decimal_places=2, editable=False, max_digits=8, help_text='\u4e0a\u6b21\u4ef7\u683c', null=True, verbose_name='\u4e0a\u6b21\u4ef7\u683c')),
                ('price_update_at', models.DateTimeField(help_text='\u5957\u9910\u4ef7\u683c\u66f4\u65b0\u65f6\u95f4', verbose_name='\u5957\u9910\u4ef7\u683c\u66f4\u65b0\u65f6\u95f4', editable=False)),
                ('sequence', models.SmallIntegerField(default=0, help_text='\u5e8f\u53f7\u8d8a\u5927\u6392\u8d8a\u524d\uff0c\u8303\u56f4\u4e3a-999~999', verbose_name='\u6392\u5e8f\u53f7', validators=[django.core.validators.MinValueValidator(-999, '\u4e0d\u80fd\u5c0f\u4e8e999'), django.core.validators.MaxValueValidator(999, '\u4e0d\u80fd\u5927\u4e8e999')])),
                ('author', models.ForeignKey(related_name='set_meals', verbose_name='\u5957\u9910\u7f16\u8f91\u8005', to=settings.AUTH_USER_MODEL, help_text='\u5957\u9910\u7f16\u8f91\u8005')),
                ('hospital', models.ForeignKey(related_name='set_meals', verbose_name='\u8be2\u4ef7\u5957\u9910\u5173\u8054\u533b\u9662', to='hospital.Hospital', help_text='\u8be2\u4ef7\u5957\u9910\u5173\u8054\u533b\u9662')),
            ],
            options={
                'ordering': ('-id',),
                'db_table': 'set_meal',
                'verbose_name': '\u5957\u9910',
                'verbose_name_plural': '\u5957\u9910',
            },
        ),
        migrations.AlterIndexTogether(
            name='hospital',
            index_together=set([('province', 'city')]),
        ),
    ]
