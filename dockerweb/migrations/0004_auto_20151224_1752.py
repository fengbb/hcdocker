# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dockerweb', '0003_container'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='container',
            options={'verbose_name_plural': '容器管理', 'verbose_name': '容器'},
        ),
        migrations.RenameField(
            model_name='container',
            old_name='dockername',
            new_name='dockerhost',
        ),
    ]
