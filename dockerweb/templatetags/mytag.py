#-*-coding:utf-8-*-
from django import template
register=template.Library()
@register.tag(name='mytag')
def key(d, key_name):
    value = d[key_name]
    return value
key = register.filter('key', key)