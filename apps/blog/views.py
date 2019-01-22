from django.shortcuts import get_object_or_404
from django.conf import settings
from django.shortcuts import redirect
from django.views.generic import DateDetailView, ListView

from .models import Post, Category


class LatestPostsView(ListView):
    """ Return a paginated list view of posts ordered by date """
    context_object_name = 'posts'
    template_name = 'blog/post_archive.html'
    paginate_by = settings.POSTS_PER_PAGE

    def get_queryset(self):
        return Post.objects.latest_public().order_by('-is_featured', '-publish_date')


class PostsByCategoryView(LatestPostsView):
    """ Return a paginated list of posts for a given category ordered by date """
    def get_allow_empty(self):
        return True

    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        qs = super(PostsByCategoryView, self).get_queryset()
        return qs.filter(categories=self.category)

    def get_context_data(self, **kwargs):
        # Call base to get context
        context = super(PostsByCategoryView, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context


class PostDetailView(DateDetailView):
    """ Display a Blog Post. Do not show unpublished or future posts unless the user is an admin """
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'
    date_field = 'publish_date'

    def get_allow_future(self):
        """ Allow admins to view future posts """
        if self.request.user.is_staff:
            return True
        else:
            return False

    def get_queryset(self):
        """ Allow admins to view unpublished posts """
        if self.request.user.is_staff:
            return Post.objects.all()
        else:
            return Post.objects.latest_public()
