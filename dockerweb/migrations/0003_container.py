# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dockerweb', '0002_docker'),
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, primary_key=True, serialize=False)),
                ('containerid', models.CharField(verbose_name='容器号', max_length=50)),
                ('containername', models.CharField(verbose_name='容器名', max_length=30)),
                ('dockername', models.GenericIPAddressField(verbose_name='所在docker主机')),
                ('imagename', models.CharField(verbose_name='镜像名', max_length=50)),
            ],
        ),
    ]
