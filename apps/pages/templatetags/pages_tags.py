# I need template tags to build page menus
# Something where I can set get all the child pages for a given page and a depth
# Maybe something where I can get the child pages for a page's root ancestor
from django import template
from django.core.cache import cache

from ..models import Page

register = template.Library()

@register.inclusion_tag("pages/_sub_nav.inc.html")
def show_page_root_sub_nav(page):
    """ Show the sub nav for a page's root ancestor """
    if not page.is_root_node():
        root = page.get_root()
    else:
        root = page

    nodes = root.get_descendants(include_self=False)
    return {'nodes':nodes, 'selected_page':page, 'root':root}


@register.simple_tag
def get_child_pages(page):
    """ Return the child pages for a given page """
    return page.get_children()
