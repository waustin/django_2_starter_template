from __future__ import absolute_import
import datetime
from django.conf import settings
from django.db import models
from filebrowser.fields import FileBrowseField
from django.urls import reverse

from .managers import PostManager


class Category(models.Model):
    name = models.CharField(max_length=250, help_text='Max 250 characters')
    slug = models.SlugField(unique=True, help_text='Suggested value automatically generated from title.')

    description = models.TextField(
        blank=True, help_text='Optional description for the cagegory')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog_posts_by_category', kwargs={'slug': self.slug})

    class Meta:
        ordering = ('slug',)
        verbose_name_plural = "Categories"


class Post(models.Model):
    title = models.CharField(max_length=250, help_text='Max 250 characters')
    slug = models.SlugField(unique_for_date='publish_date', db_index=True,
                            help_text='Suggested value automatically generated from title. Must be unique for publish date.')
    excerpt = models.TextField(
        blank=True, help_text="A short summary. Optional")
    content = models.TextField()

    publish_date = models.DateTimeField(
        default=datetime.datetime.now, db_index=True)

    is_featured = models.BooleanField(default=False, blank=True, db_index=True,
                                      help_text='Lets you feature a blog post. Typically the most recent featured blog post will show up different')

    # Published Status Field
    is_published = models.BooleanField(default=False, blank=True, db_index=True,
                                       help_text='Controls if a blog post is published on the site')

    # Categories / Facets
    categories = models.ManyToManyField(Category, related_name='posts',
                                        help_text='The categories for the Blog Post',
                                        blank=True)

    # Post Thumbnail
    thumbnail = FileBrowseField(max_length=200,
                                directory=settings.BLOG_POST_THUMB_DIR,
                                blank=True,
                                format='image',
                                help_text='An optional thumbnail for the listing page')

    # Manager
    objects = PostManager()

    def __str__(self):
        return '%s - %s' % (self.title, self.publish_date)

    def get_absolute_url(self):
        return reverse(
            'blog_post_detail', kwargs={'year': self.publish_date.strftime('%Y'),
                                        'month': self.publish_date.strftime('%b').lower(),
                                        'day': self.publish_date.strftime('%d'),
                                        'slug': self.slug})

    class Meta:
        ordering = ('-publish_date', 'slug',)
        verbose_name = 'Blog Post'
        verbose_name_plural = 'Blog Posts'
