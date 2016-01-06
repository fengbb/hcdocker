# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dockerweb', '0006_auto_20151224_1817'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='password',
            field=models.CharField(verbose_name='密码', blank=True, max_length=10, null=True),
        ),
    ]
