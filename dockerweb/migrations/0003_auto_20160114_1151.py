# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dockerweb', '0002_auto_20160114_1056'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='bz',
            field=models.CharField(null=True, max_length=100, verbose_name='备注'),
        ),
        migrations.AlterField(
            model_name='container',
            name='containername',
            field=models.CharField(unique=True, max_length=30, verbose_name='容器名'),
        ),
        migrations.AlterField(
            model_name='container',
            name='password',
            field=models.CharField(max_length=10, verbose_name='密码'),
        ),
        migrations.AlterField(
            model_name='imagename',
            name='bz',
            field=models.CharField(null=True, max_length=100, verbose_name='备注'),
        ),
    ]
