#-*-coding:utf-8-*-
import paramiko
import re
import os
import sys
###############解决django在其他地方连接mysql，报错###############################
os.environ.setdefault("DJANGO_SETTINGS_MODULE",'docker.settings')             ###
#################################################################################
from django.conf import settings
#print(settings.DOCKERDOMAIN)
imagedomain = settings.DOCKERDOMAIN
ip = '192.168.153.86'
dockerpwd = '123456'
def sshClient(ip,dockerpwd):
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip,password=dockerpwd,username="root")
    #print(ssh)
    return ssh
def getregistryjson(sshobject):
    cmdcurl = 'curl -i -k -v https://admin:admin@%s/v2/_catalog' % (imagedomain)
    stdin,stdout,stderr = sshobject.exec_command(cmdcurl)
    #print(stdin)
    print('@@@')
    jsonresult = stdout.read().decode()
    return jsonresult
    #m = re.findall(r"repositories",jsonresult)
    #if m :
    #    print (m)
    #else:
    #    m1 = re.findall(r"502",jsonresult)
    #    if m1:
    #        print('请重启registry')
    #else:
    #    print('检查原因')
#getregistryjson(sshClient(ip,dockerpwd))