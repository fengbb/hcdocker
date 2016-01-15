# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dockerweb', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagename',
            name='departmentname',
            field=models.CharField(max_length=100, verbose_name='所属项目组'),
        ),
    ]
