from django.conf.urls import include, url
from django.contrib import admin
from dockerweb import views
from dockerweb.views import *

urlpatterns = [
    # Examples:
    # url(r'^$', 'docker.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)), #包括admin django后台管理
    url(r'^$', index), #主页
    url(r'^login/$',  login),  #登录
    #url(r'^shellinabox/', shellinabox), #暂时不用
    url(r'^logout/$',logout), #退出登录
    url(r'^base/$',base), #测试base页面
    url(r'^containers/$',containers), #containers显示页面
    url(r'^containers/list/$',containerlist), #显示containers
    url(r'^container/restart/.*$',containerrestart), #重启container
    url(r'^container/stop/.*$',containerstop), #关闭container
    url(r'^container/resetpassword/.*$',resetpassword), #重置密码
    url(r'^container/commit/.*$',containercommit), #提交container
    url(r'^container/delete/.*$',containerdelete), #删除container
    url(r'^images/registry/$',registryimage),#查看私有仓库镜像
    url(r'^containers/json/$',containersstatusjson)
    #url(r'^images/registry/json/$',registryimagesjson),#吧私有仓库json数据转换到本地，然后用ajax处理


    #url(r'^api/v1/pods',pods)
    #url(r'^thtf/', include('thtfl.urls')),
]
