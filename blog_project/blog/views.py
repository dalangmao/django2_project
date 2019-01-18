#-*- coding: utf-8 -*-
import logging

from django import forms
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login
from django.core.paginator import Paginator, EmptyPage, InvalidPage, PageNotAnInteger
from django.shortcuts import render, redirect
from django.conf import settings
from .models import *

# Create your views here.

logger = logging.getLogger('blog.views')

def global_setting(request):
    SITE_NAME = settings.SITE_NAME
    SITE_DESC = settings.SITE_DESC
    #category info
    category_list = Category.objects.all()[:1]
    #doc archive info
    archive_list = Article.objects.distinct_date()
    #ad info
    #cloud of label
    #relationship link
    #article on sorting
    #Comment on sorting
    #comment_count_list = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')
    #article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list]
    return locals()


def index(request):
    try:
        article_list = Article.objects.all()
        article_list = article_list = getPage(request, article_list, 1)
    except Exception as e:
        logger.error(e)
    return render(request, 'index.html', locals())


def article(request):
    id = request.GET.get('id', None)
    try:
        article = Article.objects.get(pk=id)
    except Article.DoesNotExit:
        return render(request, 'failure.html', {'reason': 'can not find any article'})

def archive(request):
    try:
        #first get client info
        year = request.GET.get('year', None)
        month = request.GET.get('month', None)
        article_list = Article.objects.filter(date_publish__icontains=year+''+month)
        article_list = getPage(request, article_list, 2)
    except Exception as e:
        logger.error(e)
    return render(request, 'archives.html', locals())

def getPage(request, article_list, number):
    paginator = Paginator(article_list, number)
    try:
        page = int(request.GET.get('page', 1))
        article_list = paginator.page(page)
    except (EmptyPage, InvalidPage, PageNotAnInteger):
        article_list = paginator.page(1)
    return article_list


class RegForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Username", "required": "required",}),
                               max_length=50, error_messages={"required": "username cannot null"}
                               )
    email = forms.EmailField(widget=forms.TextInput(attrs={"placeHolder": "Email", "required": "required",}),
                             max_length=50, error_messages={"required": "email cannot null"}
                             )
    url = forms.URLField(widget=forms.TextInput(attrs={"placeHolder": "Url"}),
                         max_length=100, required=False
                         )
    password = forms.CharField(widget=forms.PasswordInput(attrs={"placeHolder": "Password", "required": "required",}),
                               max_length=20, error_messages={"required": "password cannot null"}
                               )


def do_reg(request):
    try:
        if request.method == 'POST':
            reg_form = RegForm(request.POST)
            if reg_form.is_valid():
                user = User.objects.create(username=reg_form.cleaned_data["username"],
                                           email=reg_form.cleaned_data["email"],
                                           url=reg_form.cleaned_data["url"],
                                           password=make_password(reg_form.cleaned_data["password"]),
                                           )
                user.save()
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                login(request, user)
                return redirect(request.POST.get('source_url'))
            else:
                return render(request, 'failure.html', {"reason": reg_form.errors})
        else:
            reg_form = RegForm()
    except Exception as e:
        logger.error(e)
    return render(request, 'reg.html', locals())