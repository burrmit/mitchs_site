# blog/admin.py

from django.contrib import admin
from blog.models import Post
from . import models

class PostAdmin(admin.ModelAdmin):
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

admin.site.register(models.Post, PostAdmin)
