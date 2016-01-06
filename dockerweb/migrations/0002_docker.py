# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dockerweb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Docker',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(verbose_name='主机名', max_length=30)),
                ('describe', models.CharField(verbose_name='主机描述', max_length=50)),
                ('user', models.ForeignKey(to='dockerweb.User')),
            ],
            options={
                'verbose_name': '主机',
                'verbose_name_plural': '主机管理',
            },
        ),
    ]
