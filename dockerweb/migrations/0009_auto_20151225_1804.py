# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dockerweb', '0008_container_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='container',
            name='containerid',
            field=models.CharField(verbose_name='容器号', max_length=100),
        ),
    ]
