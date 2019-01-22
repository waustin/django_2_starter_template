from django.conf import settings
from django.db import models
from filebrowser.fields import FileBrowseField


class BannerGroup(models.Model):
    slug = models.SlugField(unique=True, help_text='Unique Identifier for a group of banners')
    description = models.TextField(blank=True, help_text='Optional description to know what this group is used for')

    def __str__(self):
        return self.slug


class Banner(models.Model):
    title = models.CharField(max_length=150)
    sub_heading = models.CharField(max_length=250, blank=True, help_text='An optional sub heading / short teaser')
    image = FileBrowseField(max_length=200,
                            directory=settings.PROMOTIONS_BANNER_IMAGE_DIR,
                            format='image',
                            help_text='Banner image. This will be cropped to fit the size needed for the banner group')
    url = models.CharField(max_length=250, blank=True,
                           help_text='Optional URL that the banner can link to')
    url_name = models.CharField(max_length=50, blank=True,
                                help_text='Optional display text to be used for the link. May not be used in all banner groups.')
    display_order = models.PositiveIntegerField(db_index=True, default=1,
                                                help_text='Controls the order that banners are displayed')

    groups = models.ManyToManyField(BannerGroup, blank=True,
                                    help_text='The groups that this banner belongs to. This decides where a banner shows up  on the site and how it is displayed.')

    def groups_string(self):
        return ",".join([x.slug for x in self.groups.all()])
    groups_string.short_description = "Banner Groups"

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('display_order',)
