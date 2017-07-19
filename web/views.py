# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.shortcuts import render
from models import BlogPost, Subject, Tag


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
