# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import urllib2
from urllib import quote
import json
from django.http import HttpResponse
from django.shortcuts import render

from commons.ossutils import upload_oss
from models import BlogPost, Subject, Tag

BucketName = 'shareditor-shareditor'

def index(request):
    tags = Tag.objects.all()
    latest_blog_posts = BlogPost.objects.order_by('create_time').reverse()[0:5]
    hottest_blog_posts = BlogPost.objects.order_by('pv').reverse()[0:5]
    return render(request, 'web/index.html', {'tags': tags, 'latest_blog_posts': latest_blog_posts,
                                              'hottest_blog_posts': hottest_blog_posts})


def blog_list_by_tag(request):
    if 'tagname' in request.GET:
        tag_name = request.GET['tagname']
        blog_posts = BlogPost.objects.filter(tags__name=tag_name)
        latest_blog_posts = BlogPost.objects.order_by('create_time')[0:5]
        hottest_blog_posts = BlogPost.objects.order_by('pv').reverse()[0:5]
        return render(request, 'web/blog_list_by_tag.html', {'tag_name': tag_name, 'blog_posts': blog_posts,
                                                             'latest_blog_posts': latest_blog_posts,
                                                             'hottest_blog_posts': hottest_blog_posts})
    else:
        return HttpResponse('404')


def blog_show(request):
    if 'blogId' in request.GET:
        blog_id = request.GET['blogId']
        blog_post = BlogPost.objects.get(id=blog_id)
        latest_blog_posts = BlogPost.objects.order_by('create_time')[0:5]
        hottest_blog_posts = BlogPost.objects.order_by('pv').reverse()[0:5]
        tag_blog_posts = BlogPost.objects.filter(tags__name=blog_post.tags.first())
        tags = Tag.objects.all()
        prev_blog_post = BlogPost.objects.filter(tags__name=blog_post.tags.first()).filter(id__lt=blog_post.id).order_by('id').reverse()[0:1].first()
        next_blog_post = BlogPost.objects.filter(tags__name=blog_post.tags.first()).filter(id__gt=blog_post.id).order_by('id')[0:1].first()
        return render(request, 'web/blog_show.html', {'blog_post': blog_post,
                                                      'latest_blog_posts': latest_blog_posts,
                                                      'hottest_blog_posts': hottest_blog_posts,
                                                      'tag_blog_posts': tag_blog_posts, 'tags': tags,
                                                      'prev_blog_post': prev_blog_post, 'next_blog_post': next_blog_post})
    else:
        return HttpResponse('404')


def body_upload(request):
    print request.FILES
    if 'upload' in request.FILES:
        image_name = request.FILES['upload'].name
        image_content = request.FILES['upload'].read()

        url = upload_oss(BucketName, image_name, image_content)
        if url:
            return render(request, 'web/body_upload.html', {'url': url})
    return HttpResponse('upload fail')


def chatbot(request):
    latest_blog_posts = BlogPost.objects.order_by('create_time')[0:5]
    hottest_blog_posts = BlogPost.objects.order_by('pv').reverse()[0:5]
    return render(request, 'web/chatbot.html', {'latest_blog_posts': latest_blog_posts,
                                                      'hottest_blog_posts': hottest_blog_posts})


def chatbot_query(request):
    if 'input' in request.POST:
        input = request.POST['input']
        if input == '机器学习资料':
            return HttpResponse('链接: https://pan.baidu.com/s/1nuL8Lfz 密码: eqtt')
        else:
            client_ip = request.META['REMOTE_ADDR']
            url = 'http://182.92.80.220:8765/?q=' + quote(input.encode('utf-8')) + '&clientIp=' + client_ip
            response = urllib2.urlopen(url)
            json_obj = json.load(response)
            total = json_obj['total']
            if total > 0:
                return HttpResponse(json_obj['result'][0]['answer'])
    return HttpResponse('我快死了，快叫我主人救我！')
