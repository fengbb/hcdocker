from django.db import models
import json

# Create your models here.
class Container(models.Model):
    username = models.CharField(u'用户名',max_length=30)
    containerid = models.CharField(u'容器号',max_length=100)
    containername = models.CharField(u'容器名',max_length=30)
    dockerhost = models.GenericIPAddressField(u'所在docker主机IP')
    containerhost = models.GenericIPAddressField(u'容器IP地址')
    imagename = models.CharField(u'镜像名',max_length=50)
    password = models.CharField(u'密码',max_length=10,null=True)
    #status = models.CharField(u'状态',max_length=50,null=True,blank=True)

    def __str__(self):
        return self.containerid
    class Meta:
        verbose_name = '容器'
        verbose_name_plural = '容器管理'
class DockerHost(models.Model):
    ip = models.GenericIPAddressField(u'docker主机IP')
    hostpassword = models.CharField(u'docker主机密码',max_length=30)
    def __str__(self):
        return self.ip
    class Meta:
        verbose_name = 'docker主机'
        verbose_name_plural = 'docker主机管理'
class ContainerIp(models.Model):
    ip = models.GenericIPAddressField(u'container主机可以获取的IP')
    used = models.IntegerField(u'是否已经使用',default=0)#ip是否被使用0，没有使用，1已经使用
    def __str__(self):
        return self.ip
    class Meta:
        verbose_name = '容器IP'
        verbose_name_plural = '容器IP管理'
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