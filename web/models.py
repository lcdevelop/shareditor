# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


class Subject(models.Model):
    name = models.CharField(max_length=255, verbose_name='类别名称')
    introduce = models.CharField(max_length=255, verbose_name='类别简介')
    image = models.ImageField(verbose_name='类别图片')


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='标签名称')


class BlogPost(models.Model):
    title = models.CharField(max_length=255, verbose_name='文章标题')
    body = models.TextField(verbose_name='文章内容')
    create_time = models.DateTimeField(verbose_name='创建时间')
    subject = models.ForeignKey(Subject, verbose_name='类别', null=True)
    tags = models.ManyToManyField(Tag, verbose_name='标签')


