# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from models import BlogPost, Subject, Tag


def index(request):
    tags = Tag.objects.all()
    latest_blog_posts = BlogPost.objects.order_by('create_time')[0:5]
    return render(request, 'web/index.html', {'tags': tags, 'latest_blog_posts': latest_blog_posts})
