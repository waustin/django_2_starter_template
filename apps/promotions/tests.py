from django.test import TestCase

from promotions.models import Banner, BannerGroup


class PromotionsTestBase(TestCase):
    def setUp(self):
        self.group_1 = BannerGroup.objects.create(
            slug='BANNER_GROUP_1', description='Banner Group 1')
        self.group_2 = BannerGroup.objects.create(slug='BANNER_SET_2')
        self.group_3 = BannerGroup.objects.create(slug='BANNER_SET_3')

        self.banner_1 = Banner.objects.create(title='Banner 1',
                                              sub_heading='Banner 1 Heading',
                                              url='http://www.cjrw.com',
                                              display_order=2)
        self.banner_1.groups.add(self.group_1)

        self.banner_2 = Banner.objects.create(title='Banner 2',
                                              url='http://www.cjrw.com',
                                              display_order=1)
        self.banner_2.groups.add(self.group_1)
        self.banner_2.groups.add(self.group_2)

        self.banner_3 = Banner.objects.create(title='Banner 3',
                                              url='http://www.cjrw.com')
        self.banner_3.groups.add(self.group_2)
        self.banner_3.groups.add(self.group_3)


class PromotionsModelTests(PromotionsTestBase):
    def test_banner_group_create(self):
        self.assertEqual(self.group_1.__str__(), self.group_1.slug)

    def test_banner_create(self):
        self.assertEqual(self.banner_1.__str__(), self.banner_1.title)


from django.template import Template, Context


class PromotionsTemplateTagTests(PromotionsTestBase):
    def test_get_banner_by_group_tag(self):
        output = Template("""
        {% templatetag openblock %} load promotions_tags {% templatetag closeblock %}
        {% templatetag openblock %} get_banners_by_group group_slug 2 as banners {% templatetag closeblock %}
        {% templatetag openblock %} for b in banners {% templatetag closeblock %}
             {% templatetag openvariable %}b.title{% templatetag closevariable %}<br/>
        {% templatetag openblock %} endfor {% templatetag closeblock %}
        """).render(Context({'group_slug': self.group_1.slug}))

        self.assertIn(self.banner_1.title, output)
        self.assertIn(self.banner_2.title, output)
        self.assertNotIn(self.banner_3.title, output)

    def test_get_random_banner_by_group(self):
        output = Template("""
        {% templatetag openblock %} load promotions_tags {% templatetag closeblock %}
        {% templatetag openblock %} get_random_banner_by_group group_slug as banner {% templatetag closeblock %}
          {% templatetag openvariable %}banner.title{% templatetag closevariable %}<br/>
        """).render(Context({'group_slug': self.group_3.slug}))

        self.assertIn(self.banner_3.title, output)
