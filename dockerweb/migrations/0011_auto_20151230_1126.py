# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dockerweb', '0010_auto_20151230_1123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='docker',
            name='user',
        ),
        migrations.DeleteModel(
            name='Docker',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]
