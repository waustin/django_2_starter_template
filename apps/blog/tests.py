from __future__ import absolute_import
import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf import settings
from django.template import Template, Context

from blog.models import Post, Category


class BlogTestBase(TestCase):
    def setUp(self):
        self.today = datetime.datetime.now()
        self.oneday = datetime.timedelta(days=1)
        self.tomorrow = self.today + self.oneday
        self.yesterday = self.today - self.oneday
        self.category = Category.objects.create(name='Test', slug='test-cat-1')

        self.post_1 = Post.objects.create(
            title='Test Post', slug='test-post',
            is_published=True)
        self.post_1.categories.add(self.category)

        self.post_2 = Post.objects.create(
            title='Test Post 2', slug='test-post-2',
            publish_date=self.yesterday,
            is_published=True)

        self.unpub_1 = Post.objects.create(
            title='Test UnPub Post', slug='test-unpub-post')

        self.future_post = Post.objects.create(
            title='Test Post Future', slug='test-post-future',
            publish_date=self.tomorrow,
            is_published=True)


class PostModelTest(BlogTestBase):
    def test_post_create(self):
        """ Test Blog Post Creation """
        self.assertEquals(
            self.post_1.__str__(),
            "{0} - {1}".format(self.post_1.title, self.post_1.publish_date))

    def test_category_create(self):
        self.assertEquals(
            self.category.__str__(), self.category.name)

    def test_latest_public_manager(self):
        self.assertQuerysetEqual(Post.objects.latest_public(),
                                 map(repr, [self.post_1, self.post_2]))


class PostViewTests(BlogTestBase):

    def setUp(self):
        super(PostViewTests, self).setUp()

        self.admin_username = 'admin'
        self.password = 'password'
        self.admin = User.objects.create_user(username=self.admin_username,
                                              password=self.password,
                                              email='admin@example.com')
        self.admin.is_staff = True
        self.admin.save()

        self.user_username = 'user'
        self.user = User.objects.create_user(username=self.user_username,
                                             password=self.password,
                                             email='user@example.com')


class PostDetailViews(PostViewTests):
    def test_post_detail(self):
        """ Can view Published Blog Posts """
        r = self.client.get(self.post_1.get_absolute_url())

        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, 'blog/post_detail.html')
        self.assertEqual(r.context['post'], self.post_1)

    def test_post_detail_unpub(self):
        """ Test Can't view Unpublished Posts"""
        r = self.client.get(self.unpub_1.get_absolute_url())
        self.assertEqual(r.status_code, 404)
        self.assertTemplateUsed(r, '404.html')

    def test_post_detail_future(self):
        """ Test Can't View Future Posts """
        r = self.client.get(self.future_post.get_absolute_url())
        self.assertEqual(r.status_code, 404)
        self.assertTemplateUsed(r, '404.html')

    def test_admins_can_view_unpub_and_future(self):
        """ Admins can view unpublished and future posts """
        self.client.login(username=self.admin_username, password=self.password)

        r = self.client.get(self.future_post.get_absolute_url())

        self.assertEqual(r.status_code, 200, "Admin could not few future post")
        self.assertTemplateUsed(r, 'blog/post_detail.html')

        r = self.client.get(self.unpub_1.get_absolute_url())

        self.assertEqual(r.status_code, 200, "Admin could not few unpublisehd post")
        self.assertTemplateUsed(r, 'blog/post_detail.html')


class PostListViews(PostViewTests):
    def test_latest_posts(self):
        """ Anonymous Users only view 'public' posts in list """
        r = self.client.get(reverse('blog_post_latest'))

        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, 'blog/post_archive.html')
        self.assertQuerysetEqual(r.context['posts'],
                                 map(repr, [self.post_1, self.post_2]))

    def test_posts_by_category(self):
        """ Users can view private post lists by category """
        r = self.client.get(self.category.get_absolute_url())
        self.assertEqual(r.status_code, 200)
        self.assertTemplateUsed(r, 'blog/post_archive.html')
        self.assertQuerysetEqual(r.context['posts'],
                                 map(repr, [self.post_1]))
        self.assertEqual(r.context['category'], self.category)


class BlogTagsTests(BlogTestBase):
    def setUp(self):
        super(BlogTagsTests, self).setUp()
        self.category_2 = Category.objects.create(name='Test Cat 2', slug='test-cat-2')

    def test_get_latest_public_posts(self):
        tpl = Template("""
           {% templatetag openblock %} load blog_tags {% templatetag closeblock %}
           {% templatetag openblock %} get_latest_public_posts 10 as posts {% templatetag closeblock %}
        """)
        context = Context()
        tpl.render(context)
        self.assertQuerysetEqual(context['posts'],
                                 map(repr, [self.post_1, self.post_2]))

    def test_get_all_categories(self):
        tpl = Template("""
           {% templatetag openblock %} load blog_tags {% templatetag closeblock %}
           {% templatetag openblock %} get_all_categories as cats {% templatetag closeblock %}
        """)
        context = Context()
        tpl.render(context)
        self.assertQuerysetEqual(context['cats'],
                                 map(repr, [self.category, self.category_2]))

    def test_get_used_categories(self):
        tpl = Template("""
           {% templatetag openblock %} load blog_tags {% templatetag closeblock %}
           {% templatetag openblock %} get_used_categories as cats {% templatetag closeblock %}
        """)
        context = Context()
        tpl.render(context)
        self.assertQuerysetEqual(context['cats'],
                                 map(repr, [self.category]))

    def test_get_used_public_categories(self):
         tpl = Template("""
           {% templatetag openblock %} load blog_tags {% templatetag closeblock %}
           {% templatetag openblock %} get_used_public_categories as cats {% templatetag closeblock %}
        """)
        context = Context()
        tpl.render(context)
        self.assertQuerysetEqual(context['cats'],
                                 map(repr, [self.category]))
