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
from django.contrib.auth.models import User
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
                #request.session.set_expiry(60*30)
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
    cpus =''
    dockerobj = DockerHost.objects.all()
    imageadmin = ''
    imageobj = ''
    if username == 'admin':
        useradminid = User.objects.get(username='admin').id   #查询admin的id号
        useradmind = UserProfile.objects.get(user__id=useradminid).departmentname #根据登录用户id查询登录用户所属组
        imageadmin = ImageName.objects.filter(departmentname=useradmind)
        print(imageadmin)
    else:
        userid = User.objects.get(username=username).id  #查询登录用户id
        #print(userid)
        userd = UserProfile.objects.get(user__id=userid).departmentname #根据登录用户id查询登录用户所属组
        imageobj = ImageName.objects.filter(departmentname=userd)      #根据所属组，查镜像名称
        useradminid = User.objects.get(username='admin').id   #查询admin的id号
        useradmind = UserProfile.objects.get(user__id=useradminid).departmentname #根据登录用户id查询登录用户所属组
        if userd == useradmind:
            pass
        else:
            imageadmin = ImageName.objects.filter(departmentname=useradmind)
        print(imageadmin)
    if request.method == "POST":
        dockerip = request.POST.get('dockerhost') #提交的主机ip
        dockeripid = DockerHost.objects.get(ip=dockerip).id  #取到提交上来的ip对应的id号，在外键添加的时候用
        print(dockeripid)
        #print(dockerip)
        containername = request.POST.get('containername') #提交的容器名
        imagename = request.POST.get('imagename') #提交的镜像名
        print(imagename)
        pz  = request.POST.get('pz')            #提交配置信息
        bz = request.POST.get('bz')               #提交的备注
        pzcpu = pz.split(',')[0]
        pzmem = pz.split(',')[1]
        while True:
            formatobj = Format.objects.filter(ip__ip=dockerip).filter(cpunuclear=pzcpu).filter(ifexit=0) #查找对应主机上对应模板是否存在
            if formatobj:       #查询模板是否存在，存在
                print (formatobj)
                canusedformat = random.choice(formatobj)   #如果有多个一样的模板可以用，随机选择一个，解决模板满了，新建了一个模板，但是从模板中删除一个容器，现在旧模板也可以用了
                print(canusedformat)
                sumc = canusedformat.cnumber   #查询现在运行了多少台容器
                formatid = canusedformat.id     #查询模板id
                formtcpu = Format.objects.get(id=formatid) #根据模板id，查询其他值
                cpun = formtcpu.cpunuclear                  #查核数，几核
                if sumc < 6:                                         #现在运行的容器，是否小于等于6，如果小于等于6，可以创建容器
                    print(sumc,pz,pzcpu+'!'+pzmem)
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
                                notUsedIp = ContainerIp.objects.filter(used=0).filter(ip__contains=ippost3) #模糊查找，查找对应网段没有使用的ip
                                if notUsedIp:
                                    print(notUsedIp)
                                    ip = str(random.choice(notUsedIp))
                                    ipfirst = ip.split('.')[:3]
                                    #ipfirst = dockerip.split('.')[:3]
                                    ip1,ip2,ip3 = (ipfirst)
                                    print(ip1,ip2,ip3)
                                    registryup = registryjson.getregistryjson(registryjson.sshClient(dockerip,dockerpassword))
                                    m = re.findall(r"repositories",registryup)
                                    if m:
                                        if int(cpun) == 1:
                                            cpuused = formtcpu.usedcpu
                                            containerid,password = rundockercmd.createContainer(rundockercmd.sshClient(dockerip,dockerpassword),dockername=containername,imagename=imagename,containerip=ip,ip1=ip1,ip2=ip2,ip3=ip3,cpuused=cpuused,mem=pzmem)
                                        else:
                                            cpu = formtcpu.usedcpu.split('-')
                                            cpu1,cpu2 = (cpu)
                                            cpuused = '%s-%s' % (cpu1,cpu2)
                                            print(cpu1,cpu2)
                                            print(formatid)
                                            print(cpuused)
                                            print('@')
                                            containerid,password = rundockercmd.createContainer(rundockercmd.sshClient(dockerip,dockerpassword),dockername=containername,imagename=imagename,containerip=ip,ip1=ip1,ip2=ip2,ip3=ip3,cpuused=cpuused,mem=pzmem)
                                        if containerid:
                                            print(cpuused)
                                            print('$$$$$')
                                            #print(dockerip,containername, imagename,containerid,ip,password )
                                            createresult = Container.objects.create(username=username,containerid=containerid,containername=containername,dockerhost=dockerip, containerhost=ip, imagename=imagename, password=password,cpunumber_id=formatid, bz=bz)
                                            print(createresult)
                                            if createresult:
                                                ContainerIp.objects.filter(ip=ip).update(used=1)
                                                Format.objects.filter(ip__ip=dockerip).filter(cpunuclear=pzcpu).filter(ifexit=0).filter(usedcpu=canusedformat).update(cnumber=sumc+1)
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
                                    msg = '没有可用IP地址！'
                    else:
                        msg = 'docker主机ip不能为空'
                    return render_to_response('containerscreate.html',{'msg':msg})
                else:                                                  #现在运行容器数大于6，更新模板不可用
                    print('大于6个容器')
                    Format.objects.filter(ip__ip=dockerip).filter(cpunuclear=pzcpu).filter(usedcpu=canusedformat).filter(ifexit=0).update(ifexit=1)
                continue
            else:                                                    #模板不存在，先创建模板
                sumcpu = CpuInfo.objects.filter(used=0).count()#没有使用的cpu
                if sumcpu >= int(pzcpu):
                    cpuobj = CpuInfo.objects.filter(ip__ip=dockerip).filter(used=0)   #外键查询ip,查询此docker主机上没有使用的cpu号
                    #print(cpuobj)
                    for cpu in cpuobj:
                        cpus =cpus + ','+ str(cpu.cpunumber)
                    print(cpus)
                    if int(pzcpu) == 1:
                        cpu1 = cpus.split(',')[1]
                        Format.objects.create(ip_id=dockeripid,cpunuclear=pzcpu,cnumber=0,usedcpu=cpu1,ifexit=0)
                        CpuInfo.objects.filter(ip__ip=dockerip).filter(cpunumber=cpu1).update(used=1)  #模板创建成功就更新对应cpu号为不可用
                    if int(pzcpu) == 2:
                        cpu1= cpus.split(',')[1]
                        cpu2 = cpus.split(',')[2]
                        Format.objects.create(ip_id=dockeripid,cpunuclear=pzcpu,cnumber=0,usedcpu=cpu1+'-'+cpu2,ifexit=0)
                        CpuInfo.objects.filter(ip__ip=dockerip).filter(cpunumber=cpu1).update(used=1)  #模板创建成功就更新对应cpu号为不可用
                        CpuInfo.objects.filter(ip__ip=dockerip).filter(cpunumber=cpu2).update(used=1)
                    if int(pzcpu) == 4:
                        cpu1 = cpus.split(',')[1]
                        cpu2 = cpus.split(',')[2]
                        cpu3 = cpus.split(',')[3]
                        cpu4 = cpus.split(',')[4]
                        Format.objects.create(ip_id=dockeripid,cpunuclear=pzcpu,cnumber=0,usedcpu=cpu1+'-'+cpu4,ifexit=0)
                        CpuInfo.objects.filter(ip__ip=dockerip).filter(cpunumber=cpu1).update(used=1)  #模板创建成功就更新对应cpu号为不可用
                        CpuInfo.objects.filter(ip__ip=dockerip).filter(cpunumber=cpu2).update(used=1)
                        CpuInfo.objects.filter(ip__ip=dockerip).filter(cpunumber=cpu3).update(used=1)
                        CpuInfo.objects.filter(ip__ip=dockerip).filter(cpunumber=cpu4).update(used=1)
                else:
                    msg = '主机没有那么多可用cpu,请选择更低配置，或者更换主机'
                    break
                continue
        #return render_to_response('containerscreate.html',{'imageobj':imagename,'imageadmin':imageadmin})
    return render_to_response('containerscreate.html',{'msg':msg,'username':username,'dockerobj':dockerobj,'imageobj':imageobj,'imageadmin':imageadmin})
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
    print(containerip)
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
    dockerip = container.dockerhost                   #查询docker主机ip
    containerip = container.containerhost             #查询容器ip
    cpun = container.cpunumber                        #查询使用cpu号
    print(cpun)
    formatobj = Format.objects.filter(ip__ip=dockerip).filter(usedcpu=cpun) #查找对应主机上对应模板是否存在
    print(formatobj)
    for fcpu in formatobj:
        sumc = fcpu.cnumber   #查询现在运行了多少台容器
        print('*')
        print(sumc)
    docker = DockerHost.objects.get(ip=dockerip)
    dockerpassword = docker.hostpassword
    #print(dockerpassword)
    deleteresult = rundockercmd.deleteContainer(rundockercmd.sshClient(dockerip,dockerpassword),containerid)
    print(deleteresult)
    if deleteresult:
        return render_to_response('containerslist.html',{'deleteresult':deleteresult })
    else:
        try:
            container = Container.objects.get(containerid__startswith=containerid).delete()  #删除数据库
            ContainerIp.objects.filter(ip=containerip).update(used=0)
            if sumc == 6:
                print('使用达到6个cpu')
                Format.objects.filter(ip__ip=dockerip).filter(usedcpu=cpun).update(cnumber=sumc-1)
                Format.objects.filter(ip__ip=dockerip).filter(usedcpu=cpun).filter(ifexit=1).update(ifexit=0)
            else:
                print('使用没有达到6个cpu')
                Format.objects.filter(ip__ip=dockerip).filter(usedcpu=cpun).update(cnumber=sumc-1)
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
#取私有docker主机上容器的id和状态值
def containersstatusjson(request):
    alldata = ''
    dockerhostobj = DockerHost.objects.all()
    for dockerhost in dockerhostobj:
        dockerhostip = dockerhost.ip
        #print(dockerhostip)
        url = "http://%s:2375/containers/json?all=1" %(dockerhostip) #定义url地址
        #print(url)
        data = urllib.request.urlopen(url).read().decode() #取得接口json数据
        dict1 = data[1:len(data)-2]
        alldata = alldata + dict1
    #print(alldata)
    dslist = []     #docker status list 定义
    for data1 in alldata.split(','):
        m = re.findall(r'"Id":"\w+"',data1)
        if  m:
            dslist.append(m)
            #print(m)
        m1 = re.findall(r'"Status":".+"$',data1)
        if m1:
            dslist.append(m1)
            #print(m1)
    #print(dslist)
    dslistjson = json.dumps(dslist)
    #print(dslistjson)
    return HttpResponse(dslistjson,content_type='application/json')
@login_required
def registryimage(request):
    username = request.session.get('username')
    imageadmin = ''
    imageobj = ''
    if username == 'admin':
        useradminid = User.objects.get(username='admin').id   #查询admin的id号
        useradmind = UserProfile.objects.get(user__id=useradminid).departmentname #根据登录用户id查询登录用户所属组
        imageobj = ImageName.objects.all()

    else:
        userid = User.objects.get(username=username).id  #查询登录用户id
        print(userid)
        userd = UserProfile.objects.get(user__id=userid).departmentname #根据登录用户id查询登录用户所属组
        imageobj = ImageName.objects.filter(departmentname=userd)      #根据所属组，查镜像名称
        useradminid = User.objects.get(username='admin').id   #查询admin的id号
        useradmind = UserProfile.objects.get(user__id=useradminid).departmentname #根据登录用户id查询登录用户所属组
        imageadmin = ImageName.objects.filter(departmentname=useradmind)
        print(imageadmin)
        print(imageobj)
    return render_to_response('registryimage.html',{'username':username,'imageobj':imageobj,'imageadmin':imageadmin})