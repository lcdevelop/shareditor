# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField


class Subject(models.Model):
    name = models.CharField(max_length=255, verbose_name='类别名称')
    introduce = models.CharField(max_length=255, verbose_name='类别简介')
    image = models.ImageField(max_length=255, verbose_name='类别图片', null=True)

    class Meta:
        verbose_name_plural = '类别'

    def __unicode__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='标签名称')
    image = models.ImageField(max_length=255, verbose_name='标签图片', null=True)
    sort = models.IntegerField(verbose_name='排序越大越靠前', default=0)
    show = models.IntegerField(verbose_name='是否展示在首页', default=1)

    def get_latest_blogpost(self, count=5):
        return self.blogpost_set.filter(verify=True).order_by('id').reverse()[0:count]

    class Meta:
        verbose_name_plural = '标签'

    def __unicode__(self):
        return self.name


class BlogPost(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, verbose_name='文章标题')
    image = models.ImageField(max_length=255, verbose_name='文章图片', null=True)
    abstract = models.CharField(max_length=255, verbose_name='文章摘要', null=True)
    body = RichTextUploadingField(config_name='default', verbose_name='文章内容')
    create_time = models.DateTimeField(verbose_name='创建时间')
    subject = models.ForeignKey(Subject, verbose_name='类别', null=True)
    tags = models.ManyToManyField(Tag, verbose_name='标签', null=True)
    pv = models.IntegerField(verbose_name='pv', default=0)
    verify = models.BooleanField(verbose_name='是否生效', default=False)

    def get_simple_title(self):
        return self.title.replace(self.tags.first().name, '')

    class Meta:
        verbose_name_plural = '文章'

    def __unicode__(self):
        return self.title


class Chat(models.Model):
    client_ip = models.CharField(max_length=16, verbose_name='用户ip')
    message = models.TextField(verbose_name='说的话')
    talker = models.IntegerField(verbose_name='说话者:0-机器人;1-用户')
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class CorpusQuestion(models.Model):
    text = models.CharField(max_length=512, verbose_name='问')
    bad = models.IntegerField(verbose_name='踩', default=0)
    is_del = models.IntegerField(verbose_name='1-删除；0-正常', default=0)

    def __unicode__(self):
        return self.text


class CorpusAnswer(models.Model):
    text = models.CharField(max_length=512, verbose_name='答')
    like = models.IntegerField(verbose_name='点赞量', default=0)
    is_del = models.IntegerField(verbose_name='1-删除；0-正常', default=0)
    question = models.ForeignKey(CorpusQuestion, verbose_name='问题')

    def __unicode__(self):
        return self.text
