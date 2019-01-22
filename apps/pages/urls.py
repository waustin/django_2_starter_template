from django.urls import include, re_path, path
from .views import page_detail

urlpatterns = [
    re_path(r'^(?P<relative_url>(.*))/$', page_detail, name='pages_page_detail')
]
