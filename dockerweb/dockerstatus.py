#-*-coding:utf-8-*-
import paramiko
import re
import os
import urllib.request
import json
###############解决django在其他地方连接mysql，报错###############################
os.environ.setdefault("DJANGO_SETTINGS_MODULE",'docker.settings')             ###
#################################################################################
from dockerweb.models import DockerHost
def getstatus():
    alldata = ''
    dockerhostobj = DockerHost.objects.all()
    for dockerhost in dockerhostobj:
        dockerhostip = dockerhost.ip
        print(dockerhostip)
        url = "http://%s:2375/containers/json?all=1" %(dockerhostip) #定义url地址
        print(url)
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
    print(dslistjson)
getstatus()