# blog/models.py
from django.conf import settings  # Imports Django's loaded settings
from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.urls import reverse

class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status=self.model.PUBLISHED)

    def drafts(self):
        return self.filter(status=self.model.DRAFT)

    def get_authors(self):
        User = get_user_model()
        return User.objects.filter(blog_posts__in=self).distinct()

class Topic(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,  # No duplicates!
        null=False
    )
    slug = models.SlugField(unique=True, null=False)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Post(models.Model):
    """
    Represents a blog post
    """
    DRAFT = 'draft'
    PUBLISHED = 'published'
    STATUS_CHOICES = [
        (DRAFT, 'Draft'),
        (PUBLISHED, 'Published')
    ]
    title = models.CharField(max_length=255, null=False)
    content = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)  # Sets on create
    updated = models.DateTimeField(auto_now=True, null=True)  # Updates on each save
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # The Django auth user model
        on_delete=models.PROTECT,  # Prevent posts from being deleted
        related_name='blog_posts',  # "This" on the user model
        null=False
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text='Set to "published" to make this post publicly visible',
        null=False
    )
    published = models.DateTimeField(
        null=True,
        blank=True,
        help_text='The date & time this article was published',
    )
    slug = models.SlugField(
        null=False,
        unique_for_date='published',
    )
    topics = models.ManyToManyField(
        Topic,
        related_name='blog_posts'
    )
    objects = PostQuerySet.as_manager()

    class Meta:
        # Sort by the `created` field. The `-` prefix
        # specifies to order in descending/reverse order.
        # Otherwise, it will be in ascending order.
        ordering = ['-created']

    def publish(self):
        self.status = self.PUBLISHED
        self.published = timezone.now()

    def __str__(self):
        return self.title

    def get_url(self):
        if self.published:
            return reverse(
                'post-detail',
                kwargs={
                    'slug': self.slug
                }
            )

        return reverse('post-detail', kwargs={'slug': self.slug})
