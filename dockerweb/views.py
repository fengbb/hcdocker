#-*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404, render
from django.contrib import auth
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from dockerweb import rundockercmd,registryjson
from dockerweb.models import *
import urllib.request
import random
import re
from django.contrib import messages
from django.core.paginator import Paginator
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
                return render(request,'login.html',{'login_err': u'Docker管理平台账户还未设定,请先登录后台管理界面创建账户!'})
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
        dockerip = request.POST.get('dockerhost') #提交的主机ip
        containername = request.POST.get('containername') #提交的容器名
        imagename = request.POST.get('imagename') #提交的镜像名
        bz = request.POST.get('bz')               #提交的备注
        if dockerip:
            cnexist = Container.objects.filter(containername=containername) #判断容器名是否存在
            print(dockerip,containername,imagename)
            docker = DockerHost.objects.get(ip=dockerip) #根据ip查密码
            dockerpassword = docker.hostpassword #获取主机密码
            ippost = dockerip.split('.') #吧提交的主机ip拆分
            ippost3 = ippost[2]  #取得提交主机ip的网段，根据网段获取在这个网段没有使用的ip地址
            #print(dockerpassword)
            #print(cnexist)
            if cnexist:
                msg = "容器名已存在！！！"
            else:
                sumcontainer = Container.objects.filter(username=username).count() #判断此用户有几个容器
                #print(sumcontainer)
                if int(sumcontainer) >= 10:
                    msg = "每个用户只能创建10个容器！！！"
                else:
                    while True:
                        notUsedIp = ContainerIp.objects.filter(used=0)
                        if notUsedIp:
                            ip = str(random.choice(notUsedIp))
                            ipfirst = ip.split('.')[:3]
                            #ipfirst = dockerip.split('.')[:3]
                            ip1,ip2,ip3 = (ipfirst)
                            print(ip1,ip2,ip3)
                            if ip3 == ippost3:
                                print(ippost3+'!!!!'+ip3)
                                registryup = registryjson.getregistryjson(registryjson.sshClient(dockerip,dockerpassword))
                                m = re.findall(r"repositories",registryup)
                                if m:
                                    containerid,password = rundockercmd.createContainer(rundockercmd.sshClient(dockerip,dockerpassword),containername,imagename,ip,ip1,ip2,ip3)
                                    if containerid:
                                        #print(dockerip,containername, imagename,containerid,ip,password )
                                        createresult = Container.objects.create(username=username,containerid=containerid,containername=containername,dockerhost=dockerip, containerhost=ip, imagename=imagename, password=password, bz=bz)
                                        if createresult:
                                            ContainerIp.objects.filter(ip=ip).update(used=1)
                                            msg = "容器创建成功！"
                                        else:
                                            msg = "容器创建失败！"
                                        return render_to_response('containerscreate.html',{'msg':msg,'containerid':'容器id: '+containerid,'containername':'容器名: '+containername,'ip':'容器IP地址: '+ip,'password':'容器密码: '+password})
                                    else:
                                        msg = '镜像名不存在！'
                                else:
                                    msg = '私有仓库有问题，请联管理员'
                                return render_to_response('containerscreate.html',{'msg':msg})
                            else:
                                continue
                    #return render_to_response('containerscreate.html',{'msg':msg})
                        else:
                            msg = '没有可用IP地址！'
            #return render_to_response('containerscreate.html',{'msg':msg})
        #return render_to_response('containerscreate.html',{'msg':msg})
        else:
            msg = 'docker主机ip不能为空'
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
def resetpassword(request):
    path = request.get_full_path()
    #print(path)
    containerid = path.split('/')[3][:12]
    #print(containerid)
    try:
        container = Container.objects.get(containerid__startswith=containerid)
    except :
        msg = '数据库查询有问题'
    dockername = container.containername
    print(dockername)
    dockerip = container.dockerhost
    print(dockerip)
    docker = DockerHost.objects.get(ip=dockerip)
    dockerpassword = docker.hostpassword
    print(dockerpassword)
    chagepassword = rundockercmd.resetpassword(rundockercmd.sshClient(dockerip,dockerpassword),dockername)
    print(chagepassword)
    if chagepassword:
        Container.objects.filter(containerid__startswith=containerid).update(password=chagepassword)
    else:
        msg = '重置密码错误'
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
    username = request.session.get('username')
    msg = ''
    departmentobj = Project.objects.all()
    #print(departmentobj)
    if request.method == "POST":
        path = request.get_full_path()
        #print(path)
        containerid = path.split('/')[3][:12]
        #print(containerid)
        commitimagename = request.POST.get('commitimagename')
        #print(commitimagename)
        commitdeparment = request.POST.get('department')
        print(commitdeparment)
        commitbz = request.POST.get('bz')
        print(commitbz)
        imageexist = ImageName.objects.filter(imagename=commitimagename) #判断容器名是否存在
        if imageexist:
              msg = "容器名已存在！！！"
        else:
            try:
                container = Container.objects.get(containerid__startswith=containerid)
            except :
                msg = '数据库查询有问题'
            #print(container.password,container.containername,container.containerhost,container.dockerhost)
            dockerip = container.dockerhost #获取docker主机IP地址
            docker = DockerHost.objects.get(ip=dockerip) #根据ip地址查询
            dockerpassword = docker.hostpassword #获取密码
            #print(dockerpassword)

            commitresult = rundockercmd.commitContainer(rundockercmd.sshClient(dockerip,dockerpassword),containerid,commitimagename)
            msg = 'commit 失败' + commitresult
            if commitresult:
                registryup = registryjson.getregistryjson(registryjson.sshClient(dockerip,dockerpassword))
                m = re.findall(r"repositories",registryup)
                if m:
                    print(commitresult)
                    tagresult = rundockercmd.pushImage(rundockercmd.sshClient(dockerip,dockerpassword),commitresult,commitimagename)
                    print(tagresult)
                    msg = '提交远程完成！'
                    createimage = ImageName.objects.create(username=username,imagename=commitimagename,departmentname=commitdeparment,bz=commitbz)
                else:
                    msg ='私有仓库有问题，请联管理员'
                return render_to_response('containercommit.html',{'msg':msg})
            else:
                return render_to_response('containercommit.html',{'commitresult':commitresult,'msg':msg})
            return render_to_response('containercommit.html',{'msg':msg})
        return render_to_response('containercommit.html',{'msg':msg})
    return render_to_response('containercommit.html',{'msg':msg,'departmentobj':departmentobj,'username':username})
#def registryimagesjson(request):
#    url = "https://admin:admin@hc.docker.io/v2/_catalog"  #定义url地址
#    print(url)
#    data = urllib.request.urlopen(url).read().decode() #取得接口json数据

#    print(data)
#    return HttpResponse(data,content_type='application/json')
@login_required
def registryimage(request):
    username = request.session.get('username')
    #print(username)
    useradminobj = User.objects.get(username=username)
    userid = useradminobj.id #根据username查出user id
    #print(userid)
    userobj = UserProfile.objects.get(user_id=userid)
    departmentname = userobj.departmentname#根据user id 查出外键关联的项目组

    #print(departmentname)
    if username == 'admin':
        #print('成功')
        imageobj = ImageName.objects.all()
    else:
        #print('失败')
        imageobj = ImageName.objects.filter(departmentname=departmentname) #根据项目组查出镜像
    return render_to_response('registryimage.html',{'username':username,'imageobj':imageobj})