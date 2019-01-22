from django.template import Template, Context
from django.test import TestCase
from django.utils.text import slugify
from pages.models import Page, PageTemplate


class PagesTest(TestCase):

    def test_page_creation(self):
        """ Test that a Page can be created """
        page = Page.objects.create(title=u'Test Page')
        self.assertEquals(page.title, 'Test Page')
        self.assertEquals(page.relative_url, slugify(page.title))
        self.assertEquals(page.__str__(), page.title)


    def test_pagetemnplate_creation(self):
        template = PageTemplate.objects.create(name='Template', file_name='test.html')
        page = Page.objects.create(title=u'Test Page', template=template)

        self.assertEqual(template.__str__(), template.name)


    def test_resaving_a_page_doesnt_change_url(self):
        """ Test that resaving a page does not change the url """
        parent = Page.objects.create(title="Parent Page")
        child = Page.objects.create(title=u"Child Page", parent=parent)
        self.assertEquals(parent.relative_url,'parent-page')
        self.assertEquals(child.relative_url, 'parent-page/child-page')

        parent.content = "Blah Blah"
        parent.save()
        self.assertEquals(parent.relative_url,'parent-page')

        child.meta_title = "test"
        self.assertEquals(child.relative_url, 'parent-page/child-page')

    def test_changing_page_title_doesnot_change_url(self):
        """ Test that chaning a page's title does not change the url """
        parent = Page.objects.create(title=u"Parent Page")
        child = Page.objects.create(title=u"Child Page", parent=parent)
        self.assertEquals(parent.relative_url,'parent-page')
        self.assertEquals(child.relative_url, 'parent-page/child-page')

        parent.title = "Blah Blah"
        parent.save()
        self.assertEquals(parent.relative_url,'parent-page')

        child.title = "testing"
        self.assertEquals(child.relative_url, 'parent-page/child-page')


    def test_pages_with_duplicate_urls(self):
        """ Test that pages with duplicate title get unique relative urls """
        parent = Page.objects.create(title=u"Parent Page")
        child = Page.objects.create(title=u"Child Page", parent=parent)

        parent_1 = Page.objects.create(title=u"Parent Page")
        child_1 = Page.objects.create(title=u"Child Page", parent=parent_1)

        child_2 = Page.objects.create(title=u"Child Page", parent=parent)

        parent_2 = Page.objects.create(title=u"Parent Page")


        self.assertEquals(parent.relative_url,'parent-page')
        self.assertEquals(child.relative_url, 'parent-page/child-page')
        self.assertEquals(parent_1.relative_url, 'parent-page-1')
        self.assertEquals(parent_2.relative_url, 'parent-page-2')
        self.assertEquals(child_1.relative_url, 'parent-page-1/child-page')
        self.assertEquals(child_2.relative_url, 'parent-page/child-page-1')



    def test_child_page_createion(self):
        """ Test that a Child page can be created """
        parent = Page.objects.create(title=u"Parent Page",)
        child = Page.objects.create(title=u"Child Page", parent=parent)
        self.assertEquals(child.title, 'Child Page')
        self.assertEquals(child.__str__(), child.title)
        self.assertEquals(child.relative_url, 'parent-page/child-page')

    def test_page_fetch(self):
        """ Test that the page view works """
        page = Page.objects.create(title=u'Test Page')

        response = self.client.get(page.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page'], page)

        # Test with explicit template set
        template = PageTemplate.objects.create(name='Template', file_name='pages/default.html')
        page.template = template
        page.save()

        response = self.client.get(page.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['page'], page)

    def test_hidden_pages_return_404(self):
        # Hidden pages return a 404
        page = Page.objects.create(title=u'Test Page',
                                   is_hidden=True)
        page.save()
        response = self.client.get(page.get_absolute_url())
        self.assertEqual(response.status_code, 404)



class PagesTemplateTagsTest(TestCase):
    def setUp(self):
        self.parent_1 = Page.objects.create(title=u"Parent Page 1")
        self.child_p1_1 = Page.objects.create(title=u"Child Page 1 Parent 1", parent=self.parent_1)
        self.child_p1_2 = Page.objects.create(title=u"Child Page 2 Parent 1", parent=self.parent_1)
        self.grandchild_p1_1 = Page.objects.create(title=u"Grandchild Page 1 Parent 1", parent=self.child_p1_1)

        self.parent_2 = Page.objects.create(title=u"Parent Page 2")
        self.child_p2_1 = Page.objects.create(title=u"Child Page 1 Parent 2", parent=self.parent_2, display_order=2)
        self.child_p2_2 = Page.objects.create(title=u"Child Page 2 Parent 2", parent=self.parent_2, display_order=1)

        self.parent_3 = Page.objects.create(title=u"Parent Page 3")

    def test_show_page_root_sub_nav(self):
        """ show_page_root_sub_nav displays the child page navigation
            for a page's root node """
        output = Template("""
            {% templatetag openblock %} load pages_tags {% templatetag closeblock %}
            {% templatetag openblock %} show_page_root_sub_nav page {% templatetag closeblock %}
        """).render(Context({'page':self.child_p1_1}))
        self.assertIn(self.parent_1.title, output)
        self.assertIn(self.child_p1_1.title, output)
        self.assertIn(self.child_p1_2.title, output)
        self.assertIn(self.grandchild_p1_1.title, output)
        self.assertNotIn(self.child_p2_1.title, output)

        output = Template("""
            {% templatetag openblock %} load pages_tags {% templatetag closeblock %}
            {% templatetag openblock %}show_page_root_sub_nav page {% templatetag closeblock %}
        """).render(Context({'page':self.parent_2}))

        self.assertIn(self.child_p2_1.title, output)
        self.assertIn(self.child_p2_2.title, output)
        self.assertNotIn(self.child_p1_1.title, output)

        output = Template("""
            {% templatetag openblock %} load pages_tags {% templatetag closeblock %}
            {% templatetag openblock %} show_page_root_sub_nav page {% templatetag closeblock %}
        """).render(Context({'page':self.grandchild_p1_1 }))

        self.assertIn(self.child_p1_1.title, output)
        self.assertIn(self.child_p1_2.title, output)
        self.assertIn(self.grandchild_p1_1.title, output)
        self.assertNotIn(self.child_p2_1.title, output)

    def test_get_child_pages(self):
        template = Template("""
            {% templatetag openblock %}load pages_tags {% templatetag closeblock %}
            {% templatetag openblock %} get_child_pages page as children {% templatetag closeblock %}
        """)
        context = Context({'page':self.parent_1})
        template.render(context)
        self.assertQuerysetEqual(context['children'],
                [repr(self.child_p1_1), repr(self.child_p1_2)])

        # Test display order works
        template = Template("""
            {% templatetag openblock %} load pages_tags {% templatetag closeblock %}
            {% templatetag openblock %} get_child_pages page as children {% templatetag closeblock %}
        """)
        context = Context({'page':self.parent_2})
        template.render(context)
        self.assertQuerysetEqual(context['children'],
                [repr(self.child_p2_2), repr(self.child_p2_1)])
