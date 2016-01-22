from django.db import models
from django.contrib.auth.models import User
import json

# Create your models here.
class DockerHost(models.Model):
    ip = models.GenericIPAddressField(u'docker主机IP')
    hostpassword = models.CharField(u'docker主机密码',max_length=30)
    def __str__(self):
        return self.ip
    class Meta:
        verbose_name = 'docker主机'
        verbose_name_plural = 'docker主机管理'
class Format(models.Model):                  #这个表中的字段是动态创建
    ip = models.ForeignKey(DockerHost)
    cpunuclear = models.IntegerField(u'几核') #几核容器
    cnumber = models.IntegerField(u'运行几台容器') #能跑几个容器
    usedcpu = models.CharField(u'使用的cpu号',max_length=30) #占用cpu的号
    ifexit = models.IntegerField(u'是否存在')  #是否存在此类型模板，0存在，1不存在
    def __str__(self):
        return self.usedcpu
    class Meta:
        verbose_name = '模板'
        verbose_name_plural = '模板类型'
class Container(models.Model):
    username = models.CharField(u'用户名',max_length=30)
    containerid = models.CharField(u'容器号',max_length=100)
    containername = models.CharField(u'容器名',max_length=30,unique=True)
    dockerhost = models.GenericIPAddressField(u'所在docker主机IP')
    containerhost = models.GenericIPAddressField(u'容器IP地址')
    imagename = models.CharField(u'镜像名',max_length=50)
    password = models.CharField(u'密码',max_length=10)
    #cpunumber = models.IntegerField(u'所在cpu号',null=True)
    cpunumber = models.ForeignKey(Format)
    bz = models.CharField(u'备注',max_length=100,null=True)
    #status = models.CharField(u'状态',max_length=50,null=True,blank=True)

    def __str__(self):
        return self.containerid
    class Meta:
        verbose_name = '容器'
        verbose_name_plural = '容器管理'

class ContainerIp(models.Model):
    ip = models.GenericIPAddressField(u'container主机可以获取的IP',unique=True)
    used = models.IntegerField(u'是否已经使用',default=0)#ip是否被使用0，没有使用，1已经使用
    def __str__(self):
        return self.ip
    class Meta:
        verbose_name = '容器IP'
        verbose_name_plural = '容器IP管理'
class Project(models.Model):
    username = models.OneToOneField(User)
    departmentname = models.CharField(u'项目组',max_length=30,unique=True)
    def __str__(self):
        return self.departmentname
    class Meta:
        verbose_name = '项目组'
        verbose_name_plural = '项目组管理'
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=30,unique=True)
    departmentname = models.ForeignKey(Project)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name = 'Docker管理平台账户'
        verbose_name_plural = 'Docker管理账户'
class ImageName(models.Model):
    username = models.CharField(u'提交者',max_length=30)
    imagename = models.CharField(u'镜像名称',max_length=30)
    departmentname = models.CharField(u'所属项目组',max_length=100)
    bz = models.CharField(u'备注',max_length=100,null=True)
    def __str__(self):
        return self.imagename
    class Meta:
        verbose_name = '镜像'
        verbose_name_plural = '镜像管理'
class CpuInfo(models.Model):
    ip = models.ForeignKey(DockerHost)
    cpunumber = models.IntegerField(u'主机cpu号')
    used = models.IntegerField(u'是否被使用',default=0) #cpu是否被是否，0没有,1使用
    #def __str__(self):
    #    return self.ip
    class Meta:
        verbose_name = '主机cpu'
        verbose_name_plural = '主机cpu管理'






'''
class pods(models.Model):
    name = models.CharField(max_length=30)
    generateName = models.CharField(max_length=30)
    namespace = models.CharField(max_length=30)
    selfLink  = models.CharField(max_length=30)
    uid = models.CharField(max_length=30)
    resourceVersion = models.CharField(max_length=30)
    creationTimestamp = models.CharField(max_length=30)
    run = models.CharField(max_length=30)
    containers_name = models.CharField(max_length=30)
    containers_image = models.CharField(max_length=30)
    containers_ports_containerPort = models.CharField(max_length=30)
    containers_ports_protocol = models.CharField(max_length=30)
    nodename = models.IPAddressField()
    phase = models.CharField(max_length=30)
    hostip = models.CharField(max_length=30)
    podip = models.CharField(max_length=30)
    starttime = models.CharField(max_length=30)
    image = models.CharField(max_length=30)
    imageID = models.CharField(max_length=100)
    containerID = models.CharField(max_length=100)
    def save_json(json_str):
        obj = json.loads(json_str)
        sql = 'insert into pods values (%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s%s)' % (obj['name']obj['generateName']obj['namespace']obj['selfLink']obj['uid']obj[' resourceVersion']obj['creationTimestamp']obj['run']obj['']obj['']obj['']obj['']obj['']obj['']obj['']obj['']obj['']obj['']obj['']obj[''])

'''