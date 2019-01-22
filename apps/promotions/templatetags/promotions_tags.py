from django import template
from django.core.cache import cache
from random import randint

from ..models import Banner, BannerGroup

register = template.Library()

@register.simple_tag
def get_banners_by_group(group_slug, num):
    banners = Banner.objects.filter(groups__slug=group_slug)
    return banners[:num]


@register.simple_tag
def get_random_banner_by_group(group_slug):
    banners_by_group = Banner.objects.filter(groups__slug=group_slug)
    count = banners_by_group.count()
    if count > 0:
        random_index = randint(0, count - 1)
        return banners_by_group[random_index]
    else:
        return None
