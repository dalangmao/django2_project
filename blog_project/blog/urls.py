# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     urls
   Description :
   Author :       t_lishu
   date：          1/18/2019
-------------------------------------------------
   Change Activity:
                   1/18/2019:
-------------------------------------------------
"""
__author__ = 't_lishu'
from blog_project.blog.views import *
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('archive/', archive, name='archive'),
    path('article/', article, name='article'),
    #path('comment/post', comment_post, name='comment_post')
]
