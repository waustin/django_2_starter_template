from django.views.decorators.cache import cache_page
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404, render
from pages.models import Page


@cache_page(60*5)  # CACHE PAGE URLS for 5 minutes
def page_detail(request, relative_url):
    page = get_object_or_404(Page.objects.filter(is_hidden=False).select_related('template'), relative_url=relative_url)

    if page.template:
        template_name = page.template.file_name
    else:
        template_name = 'pages/default.html'

    return render(request, template_name, {'page': page, })
