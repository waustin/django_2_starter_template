from django.conf import settings
from django.urls import include, re_path, path
from django.contrib import admin
from django.views.generic import TemplateView

from filebrowser.sites import site

app_name = "start_test"

urlpatterns = [
    # Home
    re_path(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),

    # Blog
    re_path(r'^blog/', include('blog.urls')),

    # Pages
    re_path(r'^pages/', include('pages.urls')),


    # Filebrowser, DJ Admin, & Grappelli
    re_path(r'^admin/filebrowser/', site.urls),
    path('admin/', admin.site.urls),
]

# UPLOAD MEDIA IN DEBUG
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
