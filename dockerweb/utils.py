#-*-coding:utf-8-*-
import sys
import os
import urllib.request
import json
from json import JSONEncoder
import ast
##取得docker api接口留下的json数据，转化成本机api接口，解决ajax禁止跨域访问问题
def get_image_json():
    url = "http://192.168.153.86:4243/images/json" #定义url地址
    #data = urllib.request.urlopen(url).read().decode().strip()
    data = urllib.request.urlopen(url).read().decode() #使用爬虫取得docker api接口数据
    json_data = json.dumps(data).replace('\\','')  #处理取得的数据，去掉数据中的\反斜杠
    a = len(json_data)            #json 数据长度
    json_images_data = json_data[1:a-2] # 去掉开头和结尾没有用的字符 “双引号和反斜杠\
    #print (json_images_data)
    #print(data)
    #print(json.dumps(data).replace('\\',''))
    #print(type(json.dumps(data).replace('\\','')))
    #print(type(data))
    #json_data =
    #print(type(json_data))#str
    #print (type(data))
    #print (type(json.loads(data)))

    return json_images_data
def get_image_detaile_json(imageid):
    url = "http://192.168.153.86:4243/images/%s/json" %(imageid)
    data = urllib.request.urlopen(url).read().decode()
    print (data)
    print (json.dumps(data).replace('\\','',3))
    json_data = json.dumps(data).replace('\\','')
    #print (json_data)
    a = len(json_data)
    json_images_data = json_data[1:a-2]
    #print (json_images_data)
    return json_images_data
def get_container_json():
    url = "http://192.168.153.86:4243/containers/json?all=1"
    #url = "http://192.168.153.86:4243/containers/json"
    data = urllib.request.urlopen(url).read().decode()
    json_data = json.dumps(data).replace('\\','')
    a = len(json_data)
    json_container_data = json_data[1:a-2]
    #print (json_container_data)
    return (json_container_data)

def test():
    data1 = {'b':789,'c':456,'a':123,'d':'1234'}
    d1 = json.dumps(data1,ensure_ascii = False)
    print (type(d1))
    print (d1)
    return data1
#get_image_json()
#test()
#get_container_json()
