# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dockerweb', '0005_auto_20151224_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='containerhost',
            field=models.GenericIPAddressField(verbose_name='容器IP地址'),
        ),
    ]
