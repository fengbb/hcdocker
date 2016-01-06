# -*- coding: utf-8 -*-
#from __future__ import unicode_literals

from django import forms
from django.forms.formsets import BaseFormSet, formset_factory
from dockerweb.models import User

#from django.core import validators
#注册
class UserForm(forms.Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密   码', widget=forms.PasswordInput())

class UserRegistForm(forms.Form):
    username = forms.CharField(label='用户名')
    password = forms.CharField(label='密码', widget = forms.PasswordInput())
    email = forms.EmailField(label='电子邮箱')
    def clean_email(self):
        cleaned_data=super(UserRegistForm,self).clean()
        email_data=cleaned_data.get('email')
        if User.objects.filter(email=email_data).count() is not 0:
            raise forms.ValidationError(u'邮箱已被注册,请使用其他邮箱或者找回密码')
        user_data=cleaned_data.get('username')
        if User.objects.filter(username=user_data).count() is not 0:
            raise forms.ValidationError(u'用户名已存在，请更换用户名')
        return cleaned_data
class CreateContainersForm(forms.Form):
    dockerhost = forms.CharField(label='主机IP')
    containername = forms.CharField(label='容器名')
    imagesname = forms.CharField(label='镜像名称')
