# blog/views.py

from django.shortcuts import render
from . import models
from django.db.models import Count
from django.views import View
from django.views.generic import DetailView

def home(request):
    """
    The Blog homepage
    """
    # Get last 3 posts
    latest_posts = models.Post.objects.published().order_by('-published')[:3]
    authors = models.Post.objects.published().get_authors().order_by('first_name')
    topics = models.Topic.objects.annotate(post_count=Count('blog_posts')).order_by('-post_count')
    # Add as context variable "latest_posts"
    context = {
        'topics': topics,
        'authors': authors,
        'latest_posts': latest_posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    """
    The About Me Page
    """
    topics = models.Topic.objects.annotate(post_count=Count('blog_posts')).order_by('-post_count')
    context = {
        'topics': topics,
    }
    return render(request, 'blog/about.html', context)

def posts(request):
    """
    The Blog homepage
    """
    posts = models.Post.objects.published().order_by('-published')
    authors = models.Post.objects.published().get_authors().order_by('first_name')
    topics = models.Topic.objects.annotate(post_count=Count('blog_posts')).order_by('-post_count')
    # Add as context variable "latest_posts"
    context = {
        'topics': topics,
        'authors': authors,
        'posts': posts
    }
    return render(request, 'blog/posts.html', context)

def contact(request):
    """
    The Contact Page
    """
    topics = models.Topic.objects.annotate(post_count=Count('blog_posts')).order_by('-post_count')
    context = {
        'topics': topics,
    }
    return render(request, 'blog/contact.html', context)

class PostDetailView(DetailView):
    model = models.Post
