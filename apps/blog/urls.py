from __future__ import absolute_import
from django.urls import include, re_path, path

from .views import LatestPostsView, PostsByCategoryView, PostDetailView

urlpatterns = [
    # Get Latest Blog Posts
    re_path(r'^$', LatestPostsView.as_view(),
        name='blog_post_latest'),

    # List News stories by a categroy
    re_path(r'^category/(?P<slug>[-\w]+)/$',
        PostsByCategoryView.as_view(),
        name='blog_posts_by_category'),

    # Get Post Detail
    re_path(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{2})/(?P<slug>[-\w]+)/$',
        PostDetailView.as_view(),
        name='blog_post_detail'),

]
