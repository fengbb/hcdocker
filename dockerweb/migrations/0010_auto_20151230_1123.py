# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dockerweb', '0009_auto_20151225_1804'),
    ]

    operations = [
        migrations.CreateModel(
            name='DockerHost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('ip', models.GenericIPAddressField(verbose_name='docker主机IP')),
                ('hostpassword', models.CharField(verbose_name='docker主机密码', max_length=30)),
            ],
            options={
                'verbose_name': 'docker主机',
                'verbose_name_plural': 'docker主机管理',
            },
        ),
        migrations.AlterField(
            model_name='container',
            name='password',
            field=models.CharField(verbose_name='密码', null=True, max_length=10),
        ),
        migrations.AlterField(
            model_name='container',
            name='username',
            field=models.CharField(verbose_name='用户名', max_length=30),
        ),
    ]
