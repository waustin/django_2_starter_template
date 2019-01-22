from django.conf import settings
from django.db import models
from django.utils.text import slugify
from django.utils.encoding import smart_text
from django.urls import reverse

from mptt.models import MPTTModel, TreeForeignKey
from filebrowser.fields import FileBrowseField

from sitetree.models import Tree as SiteTree


class PageTemplate(models.Model):
    """ Template for a page. Helps to easily customize the page in the admin """
    name = models.CharField(max_length=100, unique=True, help_text='Unique Name/ID for a template.')
    file_name = models.CharField(max_length=100, help_text='Full Path and file name of the template.')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Page(MPTTModel):
    title = models.CharField(max_length=100)
    relative_url = models.CharField(
        max_length=250, unique=True,
        db_index=True, editable=False)

    display_order = models.PositiveIntegerField(default=1,
                                                db_index=True,
                                                help_text='Controls order that pages are displayed')

    parent = TreeForeignKey(
        'self', null=True, blank=True, related_name='children', on_delete=models.SET_NULL)

    content = models.TextField(blank=True)

    template = models.ForeignKey(PageTemplate, blank=True, null=True, on_delete=models.SET_NULL,
                                 help_text='The template used to display this page. If blank the default template is used.')

    head_title = models.CharField(max_length=100, blank=True, default="",
                                  help_text="Page Title for head. Max length 100 characters.")
    meta_description = models.CharField(max_length=200, blank=True, default="",
                                        help_text="Page Meta Description Field. Max length 200 characters.")

    header_image = FileBrowseField(max_length=200,
                                   blank=True,
                                   directory=settings.PAGES_HEADER_IMAGE_DIR,
                                   format='image',
                                   help_text='Header image for the top of the page.')

    nav_menu = models.ForeignKey(SiteTree,
                                 blank=True, null=True,
                                 on_delete=models.SET_NULL,
                                 help_text='An Optional navigation menu to display on this page.')

    is_hidden = models.BooleanField(default=False, blank=True,
                                    help_text='Hidden pages do not show up in search or have a valid URL. They are useful for grouping similar pages by a parent page you don\'t want vislbe on the site')

    def save(self, *args, **kwargs):
        if not self.pk:
            # Create a new slug from the title the first time a page is saved
            tmp_slug = slugify(smart_text(self.title))
        else:
            # For exsiting objects get the last part of the url for the slug
            tmp_slug = self.relative_url.split('/')[-1]

        if self.is_child_node():
            parent_url = self.parent.relative_url
            self.relative_url = parent_url + '/' + tmp_slug
        else:
            self.relative_url = tmp_slug

        # Check for unique relative url
        queryset = Page.objects.all()
        if self.pk:
            # Exclude Self from search
            queryset = queryset.exclude(pk=self.pk)

        relative_url = self.relative_url
        cnt = 1
        while queryset.filter(relative_url=relative_url).exists():
            relative_url = self.relative_url + '-%d' % cnt
            cnt = cnt + 1

        # Found a good URL save it
        self.relative_url = relative_url

        # Save the Page
        super(Page, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('pages_page_detail', kwargs={'relative_url': self.relative_url})

    class MPTTMeta:
        order_insertion_by = ('display_order',)

    class Meta:
        ordering = ('lft',)
