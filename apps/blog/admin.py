from __future__ import absolute_import
from django import forms
from django.contrib import admin
from django.conf import settings

from .models import Post, Category


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=forms.widgets.Textarea(attrs={'class': 'mceEditor'}))


class PostAdmin(admin.ModelAdmin):
    form = PostAdminForm
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('publish_date', 'categories', 'is_published', 'is_featured')
    list_display = ('title', 'publish_date', 'is_published', 'is_featured')
    date_hierarchy = 'publish_date'
    filter_horizontal = ('categories',)
    search_fields = ('title', 'content', 'excerpt',)

    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'publish_date', 'excerpt',),
            'classes': ('mceEditor',),
        }),
        ('Body Content', {
            'fields': ('content',),
            'classes': ('full-width',),
        }),
        ('Images', {
            'fields': ('thumbnail',),
        }),
        ('Categorization', {
            'fields': ('categories', 'is_featured'),
        }),
        ('Published Status', {
            'fields': ('is_published',),
        }),
    )

    # Admin actions
    actions = ('make_published', 'make_draft',)

    # An Admin action to make a story published
    def make_published(self, request, queryset):
        rows_updated = queryset.update(is_published=True)
        if rows_updated == 1:
            message_bit = "1 object was"
        else:
            message_bit = "%s objects were" % rows_updated
        self.message_user(request, "%s successfully marked as published." % message_bit)
    make_published.short_description = "Mark selected as published"

    # An Admin action to make a story draft
    def make_draft(self, request, queryset):
        rows_updated = queryset.update(is_published=False)
        if rows_updated == 1:
            message_bit = "1 object was"
        else:
            message_bit = "%s objects were" % rows_updated
        self.message_user(request, "%s successfully marked as draft." % message_bit)
    make_draft.short_description = "Mark selected as draft"

    class Media:
        js = (settings.STATIC_URL + 'tiny_mce/tiny_mce.js',
              settings.STATIC_URL + 'js/tiny_mce_init.js')


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
