# blog/admin.py

from django.contrib import admin
from blog.models import Post, Comment
from . import models

class CommentInline(admin.StackedInline):
    model = Comment
    readonly_fields = ('name','email','text')
    can_delete = False
    extra = 0

class PostAdmin(admin.ModelAdmin):
    inlines = [
        CommentInline,
    ]

    list_display = (
        'title',
        'author',
        'status',
        'created',
        'updated',
    )

    list_filter = (
        'status',
        'topics',
    )

    search_fields = (
        'title',
        'author__username',
        'author__first_name',
        'author__last_name',
    )

    prepopulated_fields = {'slug': ('title',)}

@admin.register(models.Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug',
    )
    prepopulated_fields = {'slug': ('name',)}

@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        'post',
        'text',
        'name',
        'email',
        'created',
    )
    search_fields = (
        'name',
        'email',
        'text',
        'approved',
    )
    list_filter = (
        'approved',
    )

admin.site.register(models.Post, PostAdmin)
