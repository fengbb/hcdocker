#-*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, render
from django.contrib import auth
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from dockerweb import rundockercmd
from dockerweb.models import *
import urllib.request
import random
from django.contrib import messages
@login_required
def index(request):
    username = request.session.get('username')
    #print (username)
    return render_to_response('index.html',{'username':username})
def base(request):
    username = request.POST.get('username')
    return render_to_response('base.html',{'username':username})
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        #print (username)
        #print (password)
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            try:
                auth.login(request,user)
                request.session.set_expiry(60*30)
                request.session['username'] = username
                #print 'session expires at :',request.session.get_expiry_date()
                return HttpResponseRedirect('/')
            except ObjectDoesNotExist:
                return render(request,'login.html',{'login_err': u'CrazyEye账户还未设定,请先登录后台管理界面创建CrazyEye账户!'})
        else:
            return render(request,'login.html',{'login_err': 'Wrong username or password!'})
    else:
        return render(request, 'login.html')
@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect("/")
@login_required
def containers(request):
    username = request.session.get('username')
    msg = ''
    dockerobj = DockerHost.objects.all()
    #print(username)
    if request.method == "POST":
        dockerip = request.POST.get('dockerhost')
        containername = request.POST.get('containername')
        imagename = request.POST.get('imagename')
        cnexist = Container.objects.filter(containername=containername)
        #print(dockerip,containername,imagename)
        docker = DockerHost.objects.get(ip=dockerip)
        dockerpassword = docker.hostpassword
        #print(dockerpassword)
        #print(cnexist)
        if cnexist:
            msg = "容器名已存在！！！"
        else:
            sumcontainer = Container.objects.filter(username=username).count()
            #print(sumcontainer)
            if int(sumcontainer) >= 5:
                msg = "每个用户只能创建5个容器！！！"
            else:
                notUsedIp = ContainerIp.objects.filter(used=0)
                if notUsedIp:
                    ip = str(random.choice(notUsedIp))
                    ipfirst = ip.split('.')[:3]
                    #ipfirst = dockerip.split('.')[:3]
                    ip1,ip2,ip3 = (ipfirst)
                    print(ip1,ip2,ip3)
                    containerid,password = rundockercmd.createContainer(rundockercmd.sshClient(dockerip,dockerpassword),containername,imagename,ip,ip1,ip2,ip3)
                    #print(dockerip,containername, imagename,containerid,ip,password )
                    createresult = Container.objects.create(username=username,containerid=containerid,containername=containername,dockerhost=dockerip, containerhost=ip, imagename=imagename, password=password)
                    if createresult:
                        ContainerIp.objects.filter(ip=ip).update(used=1)
                        msg = "容器创建成功！"
                    else:
                        msg = "容器创建失败！"
                else:
                    msg = '没有可用IP地址'
            return render_to_response('containerscreate.html',{'msg':msg})
        return render_to_response('containerscreate.html',{'msg':msg})
    return render_to_response('containerscreate.html',{'msg':msg,'username':username,'dockerobj':dockerobj})
@login_required
def containerlist(request):
    username = request.session.get('username')
    #print(username)
    containerobj = Container.objects.filter(username=username) #查找用户名为登录用户的所有镜像,第一个username指数据库中的字段，第二个username指登录用户
    #containerobj = Container.objects.all()
    return render_to_response('containerslist.html',{'containerobj':containerobj,'username':username})
@login_required
def containerrestart(request):
    msg = ''
    path = request.get_full_path()
    #print(path)
    containerid = path.split('/')[3][:12]
    #print(containerid)
    try:
        container = Container.objects.get(containerid__startswith=containerid)
    except :
        msg = '数据库查询有问题'
    #print(container.password,container.containername,container.containerhost,container.dockerhost)
    dockerip = container.dockerhost
    docker = DockerHost.objects.get(ip=dockerip)
    dockerpassword = docker.hostpassword
    #print(dockerpassword)
    containerip = container.containerhost
    password = container.password
    #print(dockerip,containerip,password)
    restartresult = rundockercmd.restartContainer(rundockercmd.sshClient(dockerip,dockerpassword),dockerid=containerid,containerip=containerip,password=password)
    if restartresult:
        msg = '容器重启成功'
    else:
        msg = '容器重启失败'
    #print(restartresult)
    return render_to_response('containerslist.html',{'msg':msg})
    #return HttpResponseRedirect('/containers/list/')
@login_required
def containerstop(request):
    path = request.get_full_path()
    #print(path)
    containerid = path.split('/')[3][:12]
    #print(containerid)
    try:
        container = Container.objects.get(containerid__startswith=containerid)
    except :
        msg = '数据库查询有问题'
    #print(container.password,container.containername,container.containerhost,container.dockerhost)
    dockerip = container.dockerhost
    docker = DockerHost.objects.get(ip=dockerip)
    dockerpassword = docker.hostpassword
    #print(dockerpassword)
    stopresult = rundockercmd.stopContainer(rundockercmd.sshClient(dockerip,dockerpassword),containerid)
    #print(stopresult)
    return HttpResponseRedirect('/containers/list/')
@login_required
def containerdelete(request):
    path = request.get_full_path()
    #print(path)
    containerid = path.split('/')[3][:12]
    #print(containerid)
    try:
        container = Container.objects.get(containerid__startswith=containerid)
    except :
        msg = '数据库查询有问题'
    #print(container.password,container.containername,container.containerhost,container.dockerhost)
    dockerip = container.dockerhost
    containerip = container.containerhost
    docker = DockerHost.objects.get(ip=dockerip)
    dockerpassword = docker.hostpassword
    #print(dockerpassword)
    deleteresult = rundockercmd.deleteContainer(rundockercmd.sshClient(dockerip,dockerpassword),containerid)
    print(deleteresult)
    if deleteresult:
        return render_to_response('containerslist.html',{'deleteresult':deleteresult })
    else:
        try:
            container = Container.objects.get(containerid__startswith=containerid).delete()
            ContainerIp.objects.filter(ip=containerip).update(used=0)
            #container = Container.objects.filter(containerid=containerid).delete()
        except :
            msg = '删除数据失败'
            #print(msg)
    return HttpResponseRedirect('/containers/list/')
@login_required
def containercommit(request):
    msg = ''
    path = request.get_full_path()
    #print(path)
    containerid = path.split('/')[3][:12]
    #print(containerid)
    commitimagename = request.POST.get('commitimagename')
    #print(commitimagename)
    try:
        container = Container.objects.get(containerid__startswith=containerid)
    except :
        msg = '数据库查询有问题'
    #print(container.password,container.containername,container.containerhost,container.dockerhost)
    dockerip = container.dockerhost
    docker = DockerHost.objects.get(ip=dockerip)
    dockerpassword = docker.hostpassword
    #print(dockerpassword)
    commitresult = rundockercmd.commitContainer(rundockercmd.sshClient(dockerip,dockerpassword),containerid,commitimagename)
    msg = 'commit 失败' + commitresult
    if commitresult:
        #print(commitresult)
        tagresult = rundockercmd.pushImage(rundockercmd.sshClient(dockerip,dockerpassword),commitresult,commitimagename)
        print(tagresult)
        msg = '提交远程完成！'
    else:
        return render_to_response('containercommit.html',{'commitresult':commitresult})
    return render_to_response('containercommit.html',{'msg':msg})
def registryimagesjson(request):
    url = "http://hc.docker.io:5000/v1/search"  #定义url地址
    data = urllib.request.urlopen(url).read().decode() #取得接口json数据
    #print(data)
    return HttpResponse(data,content_type='application/json')
@login_required
def registryimage(request):
    username = request.session.get('username')
    #print(username)
    return render_to_response('registryimage.html',{'username':username})