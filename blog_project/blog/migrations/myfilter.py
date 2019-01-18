# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     myfilter
   Description :
   Author :       t_lishu
   date：          1/18/2019
-------------------------------------------------
   Change Activity:
                   1/18/2019:
-------------------------------------------------
"""
__author__ = 't_lishu'
from django import template

register = template.Library()

#define a filter to change the month to text
@register.filter

def month_to_upper(key):
    print(key)
    return ['一','二','三','四','五','六','七','八','九','十','十一','十二',][key.month-1]

#register filter
#filter name == def name
#register.filter('month_to_upper', month_to_upper)