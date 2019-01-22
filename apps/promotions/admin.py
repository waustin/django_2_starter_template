from django.contrib import admin
from django.utils.html import format_html

from filebrowser.settings import ADMIN_THUMBNAIL

from .models import BannerGroup, Banner


class BannerGroupAdmin(admin.ModelAdmin):
    list_display = ('slug', 'description')

    fieldsets = (
        (None, {
            'fields': ('slug', 'description'),
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        """ Make the slug field readonly for updates """
        if obj:  # editing an existing object
            return self.readonly_fields + ('slug',)
        else:
            return self.readonly_fields


class BannerAdmin(admin.ModelAdmin):
    search_fields = ('title', 'url', 'url_name')
    list_display = ('title', 'image_thumbnail', 'display_order', 'url', 'groups_string')
    list_filter = ('groups',)
    filter_horizontal = ('groups',)
    list_per_page = 10

    def image_thumbnail(self, obj):
        if obj.image and obj.image.filetype == 'Image':
            return format_html('<img src="%s"/>' % obj.image.version_generate(ADMIN_THUMBNAIL).url)
        else:
            return ""
    image_thumbnail.allow_tags = True
    image_thumbnail.short_description = "Thumbnail"


admin.site.register(BannerGroup, BannerGroupAdmin)
admin.site.register(Banner, BannerAdmin)
