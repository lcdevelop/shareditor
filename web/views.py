# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import urllib2
from urllib import quote
import os
import json
import re
from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings

from commons.ossutils import upload_oss
from models import BlogPost, Subject, Tag, Chat

BucketName = 'shareditor-shareditor'
report_url_pattern = re.compile(r'.*blogId=(\d+).*')


def index(request):
    tags = Tag.objects.order_by('sort').reverse()
    latest_blog_posts = BlogPost.objects.filter(verify=True).order_by('create_time').reverse()[0:5]
    hottest_blog_posts = BlogPost.objects.filter(verify=True).order_by('pv').reverse()[0:5]
    return render(request, 'web/index.html', {'tags': tags, 'latest_blog_posts': latest_blog_posts,
                                              'hottest_blog_posts': hottest_blog_posts})


def blog_list_by_tag(request):
    if 'tagname' in request.GET:
        tag_name = request.GET['tagname']
        blog_posts = BlogPost.objects.filter(verify=True, tags__name=tag_name)
        latest_blog_posts = BlogPost.objects.filter(verify=True).order_by('create_time').reverse()[0:5]
        hottest_blog_posts = BlogPost.objects.filter(verify=True).order_by('pv').reverse()[0:5]
        return render(request, 'web/blog_list_by_tag.html', {'tag_name': tag_name, 'blog_posts': blog_posts,
                                                             'latest_blog_posts': latest_blog_posts,
                                                             'hottest_blog_posts': hottest_blog_posts})
    else:
        return HttpResponse('404')


def blog_show(request):
    if 'blogId' in request.GET:
        blog_id = request.GET['blogId']
        blog_post = BlogPost.objects.get(id=blog_id)
        latest_blog_posts = BlogPost.objects.filter(verify=True).order_by('create_time').reverse()[0:5]
        hottest_blog_posts = BlogPost.objects.filter(verify=True).order_by('pv').reverse()[0:5]
        tag_blog_posts = BlogPost.objects.filter(verify=True, tags__name=blog_post.tags.first())
        tags = Tag.objects.all()
        prev_blog_post = BlogPost.objects.filter(verify=True, tags__name=blog_post.tags.first()).filter(id__lt=blog_post.id).order_by('id').reverse()[0:1].first()
        next_blog_post = BlogPost.objects.filter(verify=True, tags__name=blog_post.tags.first()).filter(id__gt=blog_post.id).order_by('id')[0:1].first()
        return render(request, 'web/blog_show.html', {'blog_post': blog_post,
                                                      'latest_blog_posts': latest_blog_posts,
                                                      'hottest_blog_posts': hottest_blog_posts,
                                                      'tag_blog_posts': tag_blog_posts, 'tags': tags,
                                                      'prev_blog_post': prev_blog_post, 'next_blog_post': next_blog_post})
    else:
        return HttpResponse('404')


def body_upload(request):
    if 'upload' in request.FILES:
        image_name = request.FILES['upload'].name
        image_content = request.FILES['upload'].read()

        url = upload_oss(BucketName, image_name, image_content)
        if url:
            return render(request, 'web/body_upload.html', {'url': url})
    return HttpResponse('upload fail')


def chatbot(request):
    """
    废弃
    :param request:
    :return:
    """
    latest_blog_posts = BlogPost.objects.order_by('create_time')[0:5]
    hottest_blog_posts = BlogPost.objects.order_by('pv').reverse()[0:5]
    return render(request, 'web/chatbot.html', {'latest_blog_posts': latest_blog_posts,
                                                      'hottest_blog_posts': hottest_blog_posts})


# 加载配好的qa词典
def load_qa_dict():
    ret = {}
    qa_data = open(os.path.join(settings.BASE_DIR, 'web/static/web/dict/qa'), "rb").readlines()
    for qa_line in qa_data:
        qa_line = qa_line.strip()
        split = qa_line.decode('utf-8').split(' ')
        if len(split) > 1:
            question = split[0]
            answer = ' '.join(split[1:])
            ret[question] = answer

    return ret

qa_dict = load_qa_dict()


def __store_chat(request, talker, message):
    client_ip = request.META['REMOTE_ADDR']
    chat = Chat(client_ip=client_ip, message=message, talker=talker)
    chat.save()


def __select_random_question():
    chats = Chat.objects.filter(talker=1)
    chat = chats[random.randint(0, chats.count()-1)]
    return chat.message


def chatbot_query(request):
    if 'input' in request.POST:
        client_ip = request.META['REMOTE_ADDR']
        input = request.POST['input']
        __store_chat(request, 1, input)
        if qa_dict.has_key(input):
            answer = qa_dict.get(input)
            __store_chat(request, 0, answer)
            question = __select_random_question()
            __store_chat(request, 0, question)
            return HttpResponse(answer + '|' + question)
        else:
            url = 'http://182.92.80.220:8765/?q=' + quote(input.encode('utf-8')) + '&clientIp=' + client_ip
            response = urllib2.urlopen(url)
            json_obj = json.load(response)
            total = json_obj['total']
            if total > 0:
                answer = json_obj['result'][0]['answer']
                __store_chat(request, 0, answer)
                question = __select_random_question()
                __store_chat(request, 0, question)
                return HttpResponse(answer + '|' + question)
    return HttpResponse('我快死了，快叫我主人救我！')


def report_pv(request):
    if 'url' in request.GET:
        url = request.GET['url']
        m = re.match(report_url_pattern, url)
        if m:
            blog_id = int(m.group(1))
            blog = BlogPost.objects.get(id=blog_id)
            blog.pv = blog.pv + 1
            blog.save()
    image_data = open(os.path.join(settings.BASE_DIR, 'web/static/web/images/onepixel.gif'), "rb").read()
    return HttpResponse(image_data, content_type="image/gif")


def chatbotv6(request):
    latest_blog_posts = BlogPost.objects.order_by('create_time')[0:5]
    hottest_blog_posts = BlogPost.objects.order_by('pv').reverse()[0:5]
    return render(request, 'web/chatbotv6.html', {'latest_blog_posts': latest_blog_posts,
                                                'hottest_blog_posts': hottest_blog_posts})
