# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dockerweb', '0004_auto_20151224_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='containerhost',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='容器IP地址'),
        ),
        migrations.AlterField(
            model_name='container',
            name='dockerhost',
            field=models.GenericIPAddressField(verbose_name='所在docker主机IP'),
        ),
    ]
