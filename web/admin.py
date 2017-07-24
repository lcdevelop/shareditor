# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import BlogPost, Subject, Tag
from commons.ossutils import upload_oss


BucketName = 'shareditor-shareditor'


class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'create_time', 'subject')
    list_display_links = ('title',)
    search_fields = ('title', 'body',)

    def save_model(self, request, obj, form, change):
        if 'image' in request.FILES:
            image_name = request.FILES['image'].name
            image_content = request.FILES['image'].read()

            url = upload_oss(BucketName, image_name, image_content)
            if url:
                obj.image = url

        super(BlogPostAdmin, self).save_model(request, obj, form, change)


class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def save_model(self, request, obj, form, change):
        if 'image' in request.FILES:
            image_name = request.FILES['image'].name
            image_content = request.FILES['image'].read()

            url = upload_oss(BucketName, image_name, image_content)
            if url:
                obj.image = url

        super(SubjectAdmin, self).save_model(request, obj, form, change)


class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)

    def save_model(self, request, obj, form, change):
        if 'image' in request.FILES:
            image_name = request.FILES['image'].name
            image_content = request.FILES['image'].read()

            url = upload_oss(BucketName, image_name, image_content)
            if url:
                obj.image = url

        super(TagAdmin, self).save_model(request, obj, form, change)


admin.site.register(BlogPost, BlogPostAdmin)
admin.site.register(Subject, SubjectAdmin)
admin.site.register(Tag, TagAdmin)

