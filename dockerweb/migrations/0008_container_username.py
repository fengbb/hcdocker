# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dockerweb', '0007_container_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='container',
            name='username',
            field=models.CharField(verbose_name='用户名', max_length=30, blank=True, null=True),
        ),
    ]
