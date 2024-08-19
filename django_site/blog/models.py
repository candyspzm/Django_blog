from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager


class Post(models.Model):
    STATUS_OPTIONS = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    tags = TaggableManager()

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True)  # unique_for_date='published')
    author = models.ForeignKey(User, related_name='blog_posts', on_delete=models.CASCADE)
    content = models.TextField()
    published = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    # status = models.BooleanField(default=False)
    status = models.CharField(max_length=15, choices=STATUS_OPTIONS, default='draft')

    class Meta:
        ordering = ('-published',)
        verbose_name = 'Пост'
        verbose_name_plural = 'Пости'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', current_app='blog',
                       args=[
                           self.published.year,
                           self.published.strftime('%m'),
                           self.published.strftime('%d'),
                           self.slug
                       ])


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    email = models.EmailField()
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return f'Comment by {self.name} on {self.post}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='')
