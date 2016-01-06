# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('username', models.CharField(max_length=30, verbose_name='用户名')),
                ('password', models.CharField(max_length=100, verbose_name='用户密码')),
                ('email', models.EmailField(max_length=254, verbose_name='电子邮箱')),
            ],
            options={
                'verbose_name': '用户',
                'verbose_name_plural': '用户管理',
            },
        ),
    ]
