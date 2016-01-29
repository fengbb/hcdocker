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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('username', models.CharField(verbose_name='用户名', max_length=30)),
                ('containerid', models.CharField(verbose_name='容器号', max_length=100)),
                ('containername', models.CharField(max_length=30, verbose_name='容器名', unique=True)),
                ('dockerhost', models.GenericIPAddressField(verbose_name='所在docker主机IP')),
                ('containerhost', models.GenericIPAddressField(verbose_name='容器IP地址')),
                ('imagename', models.CharField(verbose_name='镜像名', max_length=50)),
                ('password', models.CharField(verbose_name='密码', max_length=10)),
                ('cmem', models.IntegerField(verbose_name='容器内存大小', null=True)),
                ('ccpu', models.IntegerField(verbose_name='容器使用核数', null=True)),
                ('bz', models.CharField(verbose_name='备注', max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': '容器管理',
                'verbose_name': '容器',
            },
        ),
        migrations.CreateModel(
            name='ContainerIp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('ip', models.GenericIPAddressField(verbose_name='container主机可以获取的IP', unique=True)),
                ('used', models.IntegerField(verbose_name='是否已经使用', default=0)),
            ],
            options={
                'verbose_name_plural': '容器IP管理',
                'verbose_name': '容器IP',
            },
        ),
        migrations.CreateModel(
            name='CpuInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('cpunumber', models.IntegerField(verbose_name='主机cpu号')),
                ('used', models.IntegerField(verbose_name='是否被使用', default=0)),
            ],
            options={
                'verbose_name_plural': '主机cpu管理',
                'verbose_name': '主机cpu',
            },
        ),
        migrations.CreateModel(
            name='DockerHost',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('ip', models.GenericIPAddressField(verbose_name='docker主机IP')),
                ('hostpassword', models.CharField(verbose_name='docker主机密码', max_length=30)),
            ],
            options={
                'verbose_name_plural': 'docker主机管理',
                'verbose_name': 'docker主机',
            },
        ),
        migrations.CreateModel(
            name='Format',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('cpunuclear', models.IntegerField(verbose_name='几核')),
                ('cnumber', models.IntegerField(verbose_name='运行几台容器')),
                ('usedcpu', models.CharField(verbose_name='使用的cpu号', max_length=30)),
                ('ifexit', models.IntegerField(verbose_name='是否存在')),
                ('ip', models.ForeignKey(to='dockerweb.DockerHost')),
            ],
            options={
                'verbose_name_plural': '模板类型',
                'verbose_name': '模板',
            },
        ),
        migrations.CreateModel(
            name='ImageName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('username', models.CharField(verbose_name='提交者', max_length=30)),
                ('imagename', models.CharField(verbose_name='镜像名称', max_length=30)),
                ('departmentname', models.CharField(verbose_name='所属项目组', max_length=100)),
                ('bz', models.CharField(verbose_name='备注', max_length=100, null=True)),
            ],
            options={
                'verbose_name_plural': '镜像管理',
                'verbose_name': '镜像',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('departmentname', models.CharField(max_length=30, verbose_name='项目组', unique=True)),
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
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=30, unique=True)),
                ('departmentname', models.ForeignKey(to='dockerweb.Project')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Docker管理账户',
                'verbose_name': 'Docker管理平台账户',
            },
        ),
        migrations.AddField(
            model_name='cpuinfo',
            name='ip',
            field=models.ForeignKey(to='dockerweb.DockerHost'),
        ),
        migrations.AddField(
            model_name='container',
            name='cpunumber',
            field=models.ForeignKey(to='dockerweb.Format'),
        ),
    ]
