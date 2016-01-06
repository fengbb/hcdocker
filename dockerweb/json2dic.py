#-*-coding:utf-8-*-
import json
from json import *
data = []
with open('pods_data.json') as f:
    for line in f:
        json_string = json.dumps(line)
        data.append(json.loads(json_string))
#定义str类型strdata1
strdata1 = ''
#定义dic类型d
d = {}
for data1 in data[9:]:
    strdata1 = strdata1 + data1
#print (strdata)
strdata = strdata1.split('\n')
for i in range(len(strdata)):
    if ':' in strdata[i]:
        key,value = strdata[i].split(':',1)
        print (key,value)
        d['key'] = value
    else:
        continue
str = "\r\n"
str = str + "insert into pods(generateName,namespace,selfLink,uid,resourceVersion,creationTimestamp,run,containers_name,containers_image,containers_ports_containerPort,containers_ports_protocol,nodename,phase,hostip,podip,starttime,image,imageID,containerID) values "
str = str + "('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s');\r\n" % (d['name'],d['generateName'],d['namespace'],d['selfLink'],d['uid'],d['resourceVersion'],d['creationTimestamp'],d['run'],d['name'],d['image'],d['containerPort'],d['protocol'],d['nodename'],d['phase'],d['hostip'],d['podip'],d['starttime'],d['image'],d['imageID'],d['containerID'])
#import  codecs
#file_object = codecs.open('pods.sql','w','utf-8')
#file_object.write(str)
#file_object.close()

