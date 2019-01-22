from django.contrib import admin
from django import forms
from django.conf import settings
from .models import Page, PageTemplate


from mptt.admin import MPTTModelAdmin


class PageAdminForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.widgets.Textarea(attrs={'class': 'mceEditor',
                                             'size': '40'}),
        required=False)

    class Meta:
        model = Page
        fields = ['title', 'display_order', 'parent', 'is_hidden',
                  'content', 'template', 'head_title', 'meta_description', 'header_image', 'nav_menu']


class PageAdmin(MPTTModelAdmin):
    mptt_level_indent = 20
    list_select_related = True

    search_fields = ('title', 'content',)
    list_display = ('title', 'relative_url', 'template', 'is_hidden')
    list_filter = ('template',)

    form = PageAdminForm

    fieldsets = (
        (None, {
            'fields': ('title', 'display_order', 'parent', 'is_hidden'),
        }),
        ('Body Content', {
            'classes': ('full-width',),
            'fields': ('content',),
        }),
        ('Media', {
            'fields': ('header_image',),
        }),
        ('Navigation', {
            'fields': ('nav_menu',),
        }),
        ('Meta Information', {
            'classes': ('collapse', 'grp-collapse grp-closed'),
            'fields': ('head_title', 'meta_description')
        }),
        ('Advaced options', {
            'classes': ('collapse', 'grp-collapse grp-closed'),
            'fields': ('template', )
        }),
    )

    class Media:
        js = (settings.STATIC_URL + 'tiny_mce/tiny_mce.js',
              settings.STATIC_URL + 'js/tiny_mce_init.js')


class PageTemplateAdmin(admin.ModelAdmin):
    pass


admin.site.register(PageTemplate, PageTemplateAdmin)
admin.site.register(Page, PageAdmin)
