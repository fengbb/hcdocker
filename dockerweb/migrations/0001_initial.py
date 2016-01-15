# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Container',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('username', models.CharField(verbose_name='用户名', max_length=30)),
                ('containerid', models.CharField(verbose_name='容器号', max_length=100)),
                ('containername', models.CharField(verbose_name='容器名', max_length=30)),
                ('dockerhost', models.GenericIPAddressField(verbose_name='所在docker主机IP')),
                ('containerhost', models.GenericIPAddressField(verbose_name='容器IP地址')),
                ('imagename', models.CharField(verbose_name='镜像名', max_length=50)),
                ('password', models.CharField(null=True, verbose_name='密码', max_length=10)),
                ('bz', models.CharField(null=True, blank=True, verbose_name='备注', max_length=100)),
            ],
            options={
                'verbose_name_plural': '容器管理',
                'verbose_name': '容器',
            },
        ),
        migrations.CreateModel(
            name='ContainerIp',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('ip', models.GenericIPAddressField(unique=True, verbose_name='container主机可以获取的IP')),
                ('used', models.IntegerField(default=0, verbose_name='是否已经使用')),
            ],
            options={
                'verbose_name_plural': '容器IP管理',
                'verbose_name': '容器IP',
            },
        ),
        migrations.CreateModel(
            name='DockerHost',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('ip', models.GenericIPAddressField(verbose_name='docker主机IP')),
                ('hostpassword', models.CharField(verbose_name='docker主机密码', max_length=30)),
            ],
            options={
                'verbose_name_plural': 'docker主机管理',
                'verbose_name': 'docker主机',
            },
        ),
        migrations.CreateModel(
            name='ImageName',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('username', models.CharField(verbose_name='提交者', max_length=30)),
                ('imagename', models.CharField(verbose_name='镜像名称', max_length=30)),
                ('bz', models.CharField(null=True, blank=True, verbose_name='备注', max_length=100)),
            ],
            options={
                'verbose_name_plural': '镜像管理',
                'verbose_name': '镜像',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('departmentname', models.CharField(unique=True, verbose_name='项目组', max_length=30)),
                ('username', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': '项目组管理',
                'verbose_name': '项目组',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(unique=True, max_length=30)),
                ('departmentname', models.ForeignKey(to='dockerweb.Project')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Docker管理账户',
                'verbose_name': 'Docker管理平台账户',
            },
        ),
        migrations.AddField(
            model_name='imagename',
            name='departmentname',
            field=models.ForeignKey(to='dockerweb.Project'),
        ),
    ]
