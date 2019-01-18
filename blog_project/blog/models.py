#-*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

#custom Article manager
class ArticleManager(models.Manager):
    def distinct_date(self):
        distinct_date_list = []
        date_list = self.values('date_publish')
        for date in date_list:
            print("date:", date)
            date = date['date_publish'].strftime('%Y%m%d document archive')
            if date not in distinct_date_list:
                distinct_date_list.append(date)
        return distinct_date_list

class Tag(models.Model):
    name = models.CharField(max_length=30, verbose_name='label name')
    class Meta:
        verbose_name = 'label'
        verbose_name_plural = verbose_name
    def __unicode__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=30, verbose_name='classify name')
    index = models.IntegerField(default=999 ,verbose_name='classify sorting')
    index1 = models.IntegerField(default=999, verbose_name='classify sorting')

    class Meta:
        verbose_name = 'classify'
        verbose_name_plural = verbose_name
        ordering = ['index', 'id']
    def __unicode__(self):
        return self.name

class User(AbstractUser):
    avatar = models.FileField(upload_to='avatar/%Y%m', default='avatar/default.png', max_length=200)
    qq = models.CharField(max_length=20, blank=True, null=True, verbose_name='QQ number')
    mobile = models.CharField(max_length=11, blank=True, null=True, unique=True, verbose_name='phone number')
    url = models.URLField(max_length=100, blank=True, null=True, verbose_name='personal website')

    class Meta:
        verbose_name = 'USER'
        verbose_name_plural = verbose_name
        ordering = ['-id']
    def __unicode__(self):
        return self.avatar

class Article(models.Model):
    title = models.CharField(max_length=50, verbose_name='title')
    desc = models.CharField(max_length=50, verbose_name='description')
    content = models.TextField(verbose_name='content')
    click_count = models.IntegerField(default=0, verbose_name='click count')
    is_recommend = models.BooleanField(default=False, verbose_name='recommend condition')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='date publish')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='tag')

    objects = ArticleManager()

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = verbose_name
        ordering = ['-date_publish']

    def __unicode__(self):
        return self.title

class Comment(models.Model):
    content = models.TextField(verbose_name='content')
    username = models.CharField(max_length=30, blank=True, null=True, verbose_name='comment username')
    email = models.EmailField(max_length=50, blank=True, null=True, verbose_name='email address')
    url =  models.URLField(max_length=100, blank=True, null=True, verbose_name='personal website url')
    date_publish = models.DateTimeField(auto_now_add=True, verbose_name='date publish')
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, blank=True, null=True, on_delete=models.CASCADE)
    pid = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return self.id